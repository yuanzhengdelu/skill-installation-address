#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project Guardian - 项目扫描脚本
扫描项目代码，识别交互模式和代码依赖关系
"""

import os
import re
import json
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple

# ============== 配置 ==============
SUPPORTED_EXTENSIONS = {'.py', '.js', '.jsx', '.ts', '.tsx', '.vue', '.html'}
IGNORE_DIRS = {'node_modules', '__pycache__', '.git', 'venv', 'env', 'dist', 'build', '.next'}


# ============== 模式检测 ==============

class PatternDetector:
    """检测代码中的交互模式"""
    
    def __init__(self):
        self.save_patterns = defaultdict(list)
        self.input_patterns = defaultdict(list)
    
    def detect_save_pattern(self, content: str, filepath: str) -> List[Dict]:
        """检测保存模式"""
        patterns = []
        
        # 实时保存模式
        realtime_indicators = [
            r'onChange\s*=.*save',
            r'onInput\s*=.*save',
            r'@input\s*=.*save',
            r'\.subscribe\(.*(save|update)',
            r'debounce.*save',
            r'autoSave',
            r'valueChanged.*emit',
            r'textChanged\.connect',
            r'currentTextChanged',
        ]
        for indicator in realtime_indicators:
            if re.search(indicator, content, re.IGNORECASE):
                patterns.append({
                    'type': 'realtime',
                    'description': '实时保存',
                    'file': filepath,
                    'indicator': indicator
                })
        
        # 按钮保存模式
        button_indicators = [
            r'onClick\s*=.*save',
            r'onSubmit\s*=.*save',
            r'@click\s*=.*save',
            r'button.*save',
            r'submit.*button',
            r'clicked\.connect.*save',
            r'QPushButton.*保存',
            r'QPushButton.*Save',
        ]
        for indicator in button_indicators:
            if re.search(indicator, content, re.IGNORECASE):
                patterns.append({
                    'type': 'button',
                    'description': '按钮保存',
                    'file': filepath,
                    'indicator': indicator
                })
        
        # 关闭时保存
        close_indicators = [
            r'onClose.*save',
            r'beforeUnload.*save',
            r'closeEvent.*save',
            r'onDestroy.*save',
            r'componentWillUnmount.*save',
        ]
        for indicator in close_indicators:
            if re.search(indicator, content, re.IGNORECASE):
                patterns.append({
                    'type': 'on_close',
                    'description': '关闭时保存',
                    'file': filepath,
                    'indicator': indicator
                })
        
        return patterns
    
    def detect_input_pattern(self, content: str, filepath: str) -> List[Dict]:
        """检测输入模式"""
        patterns = []
        
        # 下拉菜单
        dropdown_indicators = [
            r'<select',
            r'QComboBox',
            r'Dropdown',
            r'Select\s*>',
            r'v-select',
            r'el-select',
        ]
        for indicator in dropdown_indicators:
            if re.search(indicator, content, re.IGNORECASE):
                patterns.append({
                    'type': 'dropdown',
                    'description': '下拉菜单',
                    'file': filepath,
                    'indicator': indicator
                })
        
        # 输入框
        input_indicators = [
            r'<input',
            r'QLineEdit',
            r'TextField',
            r'TextInput',
            r'v-model',
        ]
        for indicator in input_indicators:
            if re.search(indicator, content, re.IGNORECASE):
                patterns.append({
                    'type': 'text_input',
                    'description': '文本输入框',
                    'file': filepath,
                    'indicator': indicator
                })
        
        # 列表选择
        list_indicators = [
            r'QListWidget',
            r'ListView',
            r'ListBox',
            r'<ul.*selectable',
        ]
        for indicator in list_indicators:
            if re.search(indicator, content, re.IGNORECASE):
                patterns.append({
                    'type': 'list_select',
                    'description': '列表选择',
                    'file': filepath,
                    'indicator': indicator
                })
        
        # 复选框/单选框
        checkbox_indicators = [
            r'<input.*type=["\']checkbox',
            r'<input.*type=["\']radio',
            r'QCheckBox',
            r'QRadioButton',
            r'Checkbox',
            r'RadioButton',
        ]
        for indicator in checkbox_indicators:
            if re.search(indicator, content, re.IGNORECASE):
                patterns.append({
                    'type': 'checkbox_radio',
                    'description': '复选框/单选框',
                    'file': filepath,
                    'indicator': indicator
                })
        
        return patterns


# ============== 依赖分析 ==============

class DependencyAnalyzer:
    """分析代码依赖关系"""
    
    def __init__(self):
        self.imports = defaultdict(set)  # file -> set of imported modules
        self.exports = defaultdict(set)  # file -> set of exported symbols
        self.function_calls = defaultdict(set)  # file -> set of called functions
        self.function_defs = defaultdict(set)  # file -> set of defined functions
    
    def analyze_file(self, content: str, filepath: str):
        """分析单个文件"""
        # Python imports
        py_imports = re.findall(r'^(?:from\s+(\S+)\s+)?import\s+(.+)$', content, re.MULTILINE)
        for from_module, imports in py_imports:
            if from_module:
                self.imports[filepath].add(from_module)
            for imp in imports.split(','):
                self.imports[filepath].add(imp.strip().split(' as ')[0])
        
        # JavaScript/TypeScript imports
        js_imports = re.findall(r'import\s+.*?from\s+[\'"](.+?)[\'"]', content)
        for imp in js_imports:
            self.imports[filepath].add(imp)
        
        # 函数定义 (Python)
        py_funcs = re.findall(r'def\s+(\w+)\s*\(', content)
        for func in py_funcs:
            self.function_defs[filepath].add(func)
        
        # 函数定义 (JavaScript)
        js_funcs = re.findall(r'(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s+)?\()', content)
        for func1, func2 in js_funcs:
            if func1:
                self.function_defs[filepath].add(func1)
            if func2:
                self.function_defs[filepath].add(func2)
        
        # 类定义
        classes = re.findall(r'class\s+(\w+)', content)
        for cls in classes:
            self.function_defs[filepath].add(cls)
    
    def build_dependency_graph(self) -> Dict:
        """构建依赖图"""
        graph = {
            'files': {},
            'symbols': {}
        }
        
        for filepath, imports in self.imports.items():
            graph['files'][filepath] = {
                'imports': list(imports),
                'defines': list(self.function_defs.get(filepath, []))
            }
        
        return graph


# ============== 主扫描逻辑 ==============

def scan_project(project_path: str) -> Tuple[List[Dict], Dict]:
    """扫描项目，返回模式列表和依赖图"""
    project_path = Path(project_path)
    detector = PatternDetector()
    analyzer = DependencyAnalyzer()
    
    all_patterns = []
    
    for root, dirs, files in os.walk(project_path):
        # 跳过忽略的目录
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            ext = Path(file).suffix.lower()
            if ext not in SUPPORTED_EXTENSIONS:
                continue
            
            filepath = Path(root) / file
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except Exception:
                continue
            
            rel_path = str(filepath.relative_to(project_path))
            
            # 检测模式
            save_patterns = detector.detect_save_pattern(content, rel_path)
            input_patterns = detector.detect_input_pattern(content, rel_path)
            all_patterns.extend(save_patterns)
            all_patterns.extend(input_patterns)
            
            # 分析依赖
            analyzer.analyze_file(content, rel_path)
    
    dependency_graph = analyzer.build_dependency_graph()
    
    return all_patterns, dependency_graph


def generate_patterns_md(patterns: List[Dict]) -> str:
    """生成 patterns.md 内容"""
    save_types = defaultdict(list)
    input_types = defaultdict(list)
    
    for p in patterns:
        if p['type'] in ['realtime', 'button', 'on_close']:
            save_types[p['type']].append(p)
        else:
            input_types[p['type']].append(p)
    
    md = """# 项目交互模式

> 此文件由 Project Guardian 自动生成
> 请检查并修改以确保准确性

## 保存模式

"""
    
    save_type_names = {
        'realtime': '实时保存',
        'button': '按钮保存',
        'on_close': '关闭时保存'
    }
    
    for save_type, name in save_type_names.items():
        if save_types[save_type]:
            md += f"### {name}\n\n"
            md += "| 文件 | 检测指标 |\n"
            md += "|------|----------|\n"
            for p in save_types[save_type][:5]:  # 最多显示5个
                md += f"| `{p['file']}` | {p['indicator']} |\n"
            md += "\n"
    
    md += """## 输入模式

"""
    
    input_type_names = {
        'dropdown': '下拉菜单',
        'text_input': '文本输入框',
        'list_select': '列表选择',
        'checkbox_radio': '复选框/单选框'
    }
    
    for input_type, name in input_type_names.items():
        if input_types[input_type]:
            md += f"### {name}\n\n"
            md += "| 文件 | 检测指标 |\n"
            md += "|------|----------|\n"
            for p in input_types[input_type][:5]:
                md += f"| `{p['file']}` | {p['indicator']} |\n"
            md += "\n"
    
    md += """## 总结

基于扫描结果，建议在本项目中遵循以下规则：

1. **保存模式**：[ ] 请根据上述检测结果填写主要的保存模式
2. **输入模式**：[ ] 请根据上述检测结果填写主要的输入模式

> 请编辑此部分，明确项目应遵循的交互模式
"""
    
    return md


def generate_user_rules_md() -> str:
    """生成 user-rules.md 模板"""
    return """# 用户自定义规则

> 在此添加您希望 AI 遵守的项目规则

## 代码规范

<!-- 示例：
- 使用驼峰命名法
- 每个函数不超过50行
- 必须添加类型注解
-->

## 交互规范

<!-- 示例：
- 所有设置项使用实时保存
- 选项超过5个时使用下拉菜单
- 表单必须有"取消"按钮
-->

## 架构规范

<!-- 示例：
- UI代码与业务逻辑分离
- 所有API调用放在 api/ 目录
- 共享组件放在 components/ 目录
-->

## 其他规则

<!-- 添加任何其他需要 AI 遵守的规则 -->
"""


def main():
    parser = argparse.ArgumentParser(description='Project Guardian - 项目规则扫描器')
    parser.add_argument('--path', '-p', required=True, help='项目路径')
    parser.add_argument('--output', '-o', help='输出目录 (默认: 项目路径/.ai-guardian)')
    args = parser.parse_args()
    
    project_path = Path(args.path).resolve()
    if not project_path.exists():
        print(f"错误: 项目路径不存在: {project_path}")
        return 1
    
    output_dir = Path(args.output) if args.output else project_path / '.ai-guardian'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"正在扫描项目: {project_path}")
    print("-" * 50)
    
    patterns, dependency_graph = scan_project(project_path)
    
    print(f"检测到 {len(patterns)} 个交互模式")
    print(f"分析了 {len(dependency_graph['files'])} 个文件的依赖关系")
    
    # 生成 patterns.md
    patterns_md = generate_patterns_md(patterns)
    patterns_path = output_dir / 'patterns.md'
    with open(patterns_path, 'w', encoding='utf-8') as f:
        f.write(patterns_md)
    print(f"已生成: {patterns_path}")
    
    # 生成 relations.json
    relations_path = output_dir / 'relations.json'
    with open(relations_path, 'w', encoding='utf-8') as f:
        json.dump(dependency_graph, f, indent=2, ensure_ascii=False)
    print(f"已生成: {relations_path}")
    
    # 生成 user-rules.md (如果不存在)
    user_rules_path = output_dir / 'user-rules.md'
    if not user_rules_path.exists():
        with open(user_rules_path, 'w', encoding='utf-8') as f:
            f.write(generate_user_rules_md())
        print(f"已生成: {user_rules_path}")
    else:
        print(f"已存在: {user_rules_path} (跳过)")
    
    print("-" * 50)
    print("扫描完成！请检查生成的规则文件并根据需要修改。")
    return 0


if __name__ == '__main__':
    exit(main())
