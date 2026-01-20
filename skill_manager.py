#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能管理器 (Skill Manager)
用于启用/禁用 Antigravity 技能的命令行工具
"""

import os
import sys
from pathlib import Path


# 技能目录
SKILLS_DIR = Path(os.environ.get('USERPROFILE', '')) / '.gemini' / 'skills'

# 颜色代码 (Windows 终端)
class Colors:
    GREEN = '\033[92m'   # 启用
    RED = '\033[91m'     # 禁用
    YELLOW = '\033[93m'  # 警告
    BLUE = '\033[94m'    # 信息
    CYAN = '\033[96m'    # 标题
    RESET = '\033[0m'    # 重置
    BOLD = '\033[1m'


def enable_colors():
    """启用 Windows 终端颜色支持"""
    if sys.platform == 'win32':
        os.system('')  # 激活 ANSI 转义序列


def get_all_skills():
    """获取所有技能及其状态"""
    skills = []
    
    if not SKILLS_DIR.exists():
        print(f"{Colors.RED}错误: 技能目录不存在: {SKILLS_DIR}{Colors.RESET}")
        return skills
    
    for item in SKILLS_DIR.iterdir():
        if not item.is_dir():
            continue
        
        skill_name = item.name
        skill_file = item / 'SKILL.md'
        disabled_file = item / 'SKILL.md.disabled'
        
        if skill_file.exists():
            skills.append({
                'name': skill_name,
                'enabled': True,
                'path': item
            })
        elif disabled_file.exists():
            skills.append({
                'name': skill_name,
                'enabled': False,
                'path': item
            })
    
    return sorted(skills, key=lambda x: x['name'])


def list_skills():
    """列出所有技能"""
    skills = get_all_skills()
    
    if not skills:
        print(f"{Colors.YELLOW}没有找到任何技能{Colors.RESET}")
        return
    
    enabled_count = sum(1 for s in skills if s['enabled'])
    disabled_count = len(skills) - enabled_count
    
    print(f"\n{Colors.CYAN}{Colors.BOLD}=== 技能管理器 ==={Colors.RESET}\n")
    print(f"目录: {SKILLS_DIR}")
    print(f"总数: {len(skills)} | {Colors.GREEN}启用: {enabled_count}{Colors.RESET} | {Colors.RED}禁用: {disabled_count}{Colors.RESET}\n")
    print(f"{'状态':<8} {'技能名称':<40}")
    print("─" * 50)
    
    for skill in skills:
        if skill['enabled']:
            status = f"{Colors.GREEN}[ON]  启用{Colors.RESET}"
        else:
            status = f"{Colors.RED}[OFF] 禁用{Colors.RESET}"
        
        print(f"{status:<17} {skill['name']:<40}")
    
    print()


def enable_skill(skill_name: str):
    """启用技能"""
    skill_dir = SKILLS_DIR / skill_name
    
    if not skill_dir.exists():
        print(f"{Colors.RED}错误: 技能不存在: {skill_name}{Colors.RESET}")
        return False
    
    disabled_file = skill_dir / 'SKILL.md.disabled'
    enabled_file = skill_dir / 'SKILL.md'
    
    if enabled_file.exists():
        print(f"{Colors.YELLOW}技能已经是启用状态: {skill_name}{Colors.RESET}")
        return True
    
    if not disabled_file.exists():
        print(f"{Colors.RED}错误: 找不到技能文件: {skill_name}{Colors.RESET}")
        return False
    
    disabled_file.rename(enabled_file)
    print(f"{Colors.GREEN}[ON] 已启用技能: {skill_name}{Colors.RESET}")
    return True


def disable_skill(skill_name: str):
    """禁用技能"""
    skill_dir = SKILLS_DIR / skill_name
    
    if not skill_dir.exists():
        print(f"{Colors.RED}错误: 技能不存在: {skill_name}{Colors.RESET}")
        return False
    
    enabled_file = skill_dir / 'SKILL.md'
    disabled_file = skill_dir / 'SKILL.md.disabled'
    
    if disabled_file.exists():
        print(f"{Colors.YELLOW}技能已经是禁用状态: {skill_name}{Colors.RESET}")
        return True
    
    if not enabled_file.exists():
        print(f"{Colors.RED}错误: 找不到技能文件: {skill_name}{Colors.RESET}")
        return False
    
    enabled_file.rename(disabled_file)
    print(f"{Colors.RED}[OFF] 已禁用技能: {skill_name}{Colors.RESET}")
    return True


def toggle_skill(skill_name: str):
    """切换技能状态"""
    skill_dir = SKILLS_DIR / skill_name
    
    if not skill_dir.exists():
        print(f"{Colors.RED}错误: 技能不存在: {skill_name}{Colors.RESET}")
        return False
    
    enabled_file = skill_dir / 'SKILL.md'
    
    if enabled_file.exists():
        return disable_skill(skill_name)
    else:
        return enable_skill(skill_name)


def print_help():
    """打印帮助信息"""
    print(f"""
{Colors.CYAN}{Colors.BOLD}=== 技能管理器 - 帮助 ==={Colors.RESET}

{Colors.BOLD}用法:{Colors.RESET}
  python skill_manager.py [命令] [技能名称]

{Colors.BOLD}命令:{Colors.RESET}
  {Colors.GREEN}list{Colors.RESET}          列出所有技能及其状态
  {Colors.GREEN}on{Colors.RESET}  <技能>    启用指定技能
  {Colors.GREEN}off{Colors.RESET} <技能>    禁用指定技能
  {Colors.GREEN}toggle{Colors.RESET} <技能> 切换技能状态
  {Colors.GREEN}help{Colors.RESET}          显示此帮助信息

{Colors.BOLD}示例:{Colors.RESET}
  python skill_manager.py list
  python skill_manager.py off project-guardian
  python skill_manager.py on project-guardian
  python skill_manager.py toggle brainstorming

{Colors.BOLD}说明:{Colors.RESET}
  技能存放在: {SKILLS_DIR}
  禁用原理: 将 SKILL.md 重命名为 SKILL.md.disabled
""")


def main():
    enable_colors()
    
    if len(sys.argv) < 2:
        list_skills()
        return
    
    command = sys.argv[1].lower()
    
    if command in ['list', 'ls', 'l', '列表']:
        list_skills()
    
    elif command in ['help', 'h', '帮助', '?']:
        print_help()
    
    elif command in ['on', 'enable', '启用']:
        if len(sys.argv) < 3:
            print(f"{Colors.RED}错误: 请指定技能名称{Colors.RESET}")
            print(f"用法: python skill_manager.py on <技能名称>")
            return
        enable_skill(sys.argv[2])
    
    elif command in ['off', 'disable', '禁用']:
        if len(sys.argv) < 3:
            print(f"{Colors.RED}错误: 请指定技能名称{Colors.RESET}")
            print(f"用法: python skill_manager.py off <技能名称>")
            return
        disable_skill(sys.argv[2])
    
    elif command in ['toggle', 't', '切换']:
        if len(sys.argv) < 3:
            print(f"{Colors.RED}错误: 请指定技能名称{Colors.RESET}")
            print(f"用法: python skill_manager.py toggle <技能名称>")
            return
        toggle_skill(sys.argv[2])
    
    else:
        print(f"{Colors.RED}未知命令: {command}{Colors.RESET}")
        print(f"使用 'python skill_manager.py help' 查看帮助")


if __name__ == '__main__':
    main()
