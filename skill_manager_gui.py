#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能管理器 GUI (Skill Manager GUI)
可视化管理 Antigravity 技能的桌面应用
"""

import os
import sys
from pathlib import Path
from typing import List, Dict

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget, QListWidgetItem, QFrame,
    QMessageBox, QLineEdit, QSplitter, QTextEdit, QGroupBox
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QColor, QIcon


# 技能目录
SKILLS_DIR = Path(os.environ.get('USERPROFILE', '')) / '.gemini' / 'skills'


class SkillItem(QFrame):
    """单个技能项"""
    
    def __init__(self, skill_name: str, enabled: bool, parent=None):
        super().__init__(parent)
        self.skill_name = skill_name
        self.enabled = enabled
        self.init_ui()
    
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # 状态指示灯
        self.status_label = QLabel()
        self.status_label.setFixedSize(20, 20)
        self.update_status_style()
        layout.addWidget(self.status_label)
        
        # 技能名称
        self.name_label = QLabel(self.skill_name)
        self.name_label.setFont(QFont("Consolas", 10))
        layout.addWidget(self.name_label, 1)
        
        # 切换按钮
        self.toggle_btn = QPushButton("禁用" if self.enabled else "启用")
        self.toggle_btn.setFixedWidth(60)
        self.toggle_btn.clicked.connect(self.toggle)
        self.update_button_style()
        layout.addWidget(self.toggle_btn)
        
        self.setFrameStyle(QFrame.StyledPanel)
    
    def update_status_style(self):
        """更新状态指示灯样式"""
        if self.enabled:
            self.status_label.setStyleSheet("""
                background-color: #4CAF50;
                border-radius: 10px;
            """)
        else:
            self.status_label.setStyleSheet("""
                background-color: #757575;
                border-radius: 10px;
            """)
    
    def update_button_style(self):
        """更新按钮样式"""
        if self.enabled:
            self.toggle_btn.setText("禁用")
            self.toggle_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #d32f2f;
                }
            """)
        else:
            self.toggle_btn.setText("启用")
            self.toggle_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #388E3C;
                }
            """)
    
    def toggle(self):
        """切换技能状态"""
        skill_dir = SKILLS_DIR / self.skill_name
        enabled_file = skill_dir / 'SKILL.md'
        disabled_file = skill_dir / 'SKILL.md.disabled'
        
        try:
            if self.enabled:
                # 禁用
                enabled_file.rename(disabled_file)
                self.enabled = False
            else:
                # 启用
                disabled_file.rename(enabled_file)
                self.enabled = True
            
            self.update_status_style()
            self.update_button_style()
            
            # 通知父窗口更新统计
            if self.parent():
                main_window = self.window()
                if hasattr(main_window, 'update_stats'):
                    main_window.update_stats()
                    
        except Exception as e:
            QMessageBox.critical(self, "错误", f"操作失败: {str(e)}")


class SkillManagerWindow(QMainWindow):
    """技能管理器主窗口"""
    
    def __init__(self):
        super().__init__()
        self.skill_items: List[SkillItem] = []
        self.init_ui()
        self.load_skills()
    
    def init_ui(self):
        self.setWindowTitle("技能管理器")
        self.setMinimumSize(500, 600)
        self.resize(550, 700)
        
        # 设置深色主题
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QLineEdit {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 8px;
                color: #ffffff;
            }
            QScrollArea {
                border: none;
            }
            QFrame {
                background-color: #2d2d2d;
                border-radius: 4px;
            }
            QGroupBox {
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                color: #888888;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_label = QLabel("🛡️ 技能管理器")
        title_label.setFont(QFont("Microsoft YaHei", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 统计信息
        self.stats_label = QLabel()
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.stats_label.setStyleSheet("color: #888888; font-size: 12px;")
        main_layout.addWidget(self.stats_label)
        
        # 搜索框
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 搜索技能...")
        self.search_input.textChanged.connect(self.filter_skills)
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)
        
        # 快捷操作按钮
        btn_layout = QHBoxLayout()
        
        self.enable_all_btn = QPushButton("全部启用")
        self.enable_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        self.enable_all_btn.clicked.connect(self.enable_all)
        btn_layout.addWidget(self.enable_all_btn)
        
        self.disable_all_btn = QPushButton("全部禁用")
        self.disable_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        self.disable_all_btn.clicked.connect(self.disable_all)
        btn_layout.addWidget(self.disable_all_btn)
        
        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.refresh_btn.clicked.connect(self.load_skills)
        btn_layout.addWidget(self.refresh_btn)
        
        main_layout.addLayout(btn_layout)
        
        # 技能列表容器
        from PySide6.QtWidgets import QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.skills_container = QWidget()
        self.skills_layout = QVBoxLayout(self.skills_container)
        self.skills_layout.setSpacing(5)
        self.skills_layout.setAlignment(Qt.AlignTop)
        
        scroll_area.setWidget(self.skills_container)
        main_layout.addWidget(scroll_area, 1)
        
        # 状态栏提示
        tip_label = QLabel("提示: 点击按钮可以启用/禁用技能")
        tip_label.setStyleSheet("color: #666666; font-size: 11px;")
        tip_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(tip_label)
    
    def load_skills(self):
        """加载所有技能"""
        # 清空现有
        for item in self.skill_items:
            item.deleteLater()
        self.skill_items.clear()
        
        # 清空布局
        while self.skills_layout.count():
            child = self.skills_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        if not SKILLS_DIR.exists():
            QMessageBox.warning(self, "警告", f"技能目录不存在: {SKILLS_DIR}")
            return
        
        skills = []
        for item in SKILLS_DIR.iterdir():
            if not item.is_dir():
                continue
            
            skill_name = item.name
            skill_file = item / 'SKILL.md'
            disabled_file = item / 'SKILL.md.disabled'
            
            if skill_file.exists():
                skills.append({'name': skill_name, 'enabled': True})
            elif disabled_file.exists():
                skills.append({'name': skill_name, 'enabled': False})
        
        # 排序
        skills.sort(key=lambda x: x['name'])
        
        # 创建技能项
        for skill in skills:
            item = SkillItem(skill['name'], skill['enabled'])
            self.skill_items.append(item)
            self.skills_layout.addWidget(item)
        
        self.update_stats()
    
    def update_stats(self):
        """更新统计信息"""
        total = len(self.skill_items)
        enabled = sum(1 for item in self.skill_items if item.enabled)
        disabled = total - enabled
        
        self.stats_label.setText(
            f"总计: {total} 个技能  |  "
            f"<span style='color: #4CAF50;'>启用: {enabled}</span>  |  "
            f"<span style='color: #f44336;'>禁用: {disabled}</span>"
        )
    
    def filter_skills(self, text: str):
        """过滤技能列表"""
        text = text.lower()
        for item in self.skill_items:
            if text in item.skill_name.lower():
                item.show()
            else:
                item.hide()
    
    def enable_all(self):
        """启用所有技能"""
        reply = QMessageBox.question(
            self, "确认", "确定要启用所有技能吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            for item in self.skill_items:
                if not item.enabled:
                    item.toggle()
    
    def disable_all(self):
        """禁用所有技能"""
        reply = QMessageBox.question(
            self, "确认", "确定要禁用所有技能吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            for item in self.skill_items:
                if item.enabled:
                    item.toggle()


def main():
    app = QApplication(sys.argv)
    
    # 设置应用图标（如果有）
    # app.setWindowIcon(QIcon("icon.png"))
    
    window = SkillManagerWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
