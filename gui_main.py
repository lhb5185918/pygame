#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from gui_base import 界面基类

class 主菜单界面(界面基类):
    """游戏主菜单界面"""
    
    def __init__(self, gui):
        super().__init__(gui)
    
    def 初始化(self):
        """初始化主菜单界面"""
        self.按钮宽度 = 200
        self.按钮高度 = 50
        self.按钮间距 = 20
        
        屏幕宽度 = self.gui.屏幕.get_width()
        屏幕高度 = self.gui.屏幕.get_height()
        
        # 计算按钮起始位置
        起始x = (屏幕宽度 - self.按钮宽度) // 2
        起始y = (屏幕高度 - (self.按钮高度 + self.按钮间距) * 5) // 2
        
        # 创建主菜单按钮
        self.创建按钮(起始x, 起始y, "开始游戏", self.开始游戏)
        self.创建按钮(起始x, 起始y + (self.按钮高度 + self.按钮间距), "收藏品", self.显示收藏品)
        self.创建按钮(起始x, 起始y + (self.按钮高度 + self.按钮间距) * 2, "角色属性", self.显示角色属性)
        self.创建按钮(起始x, 起始y + (self.按钮高度 + self.按钮间距) * 3, "游戏设置", self.显示设置)
        self.创建按钮(起始x, 起始y + (self.按钮高度 + self.按钮间距) * 4, "退出游戏", self.退出游戏)
    
    def 创建按钮(self, x, y, 文本, 回调函数):
        """创建一个按钮并添加到组件列表
        
        参数:
            x: 按钮x坐标
            y: 按钮y坐标
            文本: 按钮文本
            回调函数: 点击按钮时调用的函数
        """
        按钮 = self.gui.创建按钮(x, y, self.按钮宽度, self.按钮高度, 文本, 回调函数)
        self.添加组件(按钮)
        return 按钮
    
    def 开始游戏(self):
        """开始新游戏或继续游戏"""
        print("开始游戏")
        # 切换到游戏主界面
        self.gui.切换界面("游戏主界面")
    
    def 显示收藏品(self):
        """显示收藏品界面"""
        print("显示收藏品")
        # 切换到收藏品界面
        self.gui.切换界面("收藏品界面")
    
    def 显示角色属性(self):
        """显示角色属性界面"""
        print("显示角色属性")
        # 切换到角色属性界面
        self.gui.切换界面("角色属性界面")
    
    def 显示设置(self):
        """显示游戏设置界面"""
        print("显示设置")
        # 切换到设置界面
        self.gui.切换界面("设置界面")
    
    def 退出游戏(self):
        """退出游戏"""
        print("退出游戏")
        # 调用游戏引擎退出
        self.gui.游戏引擎.退出游戏()
    
    def 绘制(self, 屏幕):
        """绘制主菜单界面
        
        参数:
            屏幕: Pygame屏幕对象
        """
        if not self.活跃:
            return
        
        # 绘制标题
        标题字体 = pygame.font.Font(None, 72)
        标题文本 = 标题字体.render("时光记忆", True, (255, 255, 255))
        标题位置 = ((屏幕.get_width() - 标题文本.get_width()) // 2, 50)
        屏幕.blit(标题文本, 标题位置)
        
        # 绘制副标题
        副标题字体 = pygame.font.Font(None, 36)
        副标题文本 = 副标题字体.render("探索童年的回忆", True, (200, 200, 200))
        副标题位置 = ((屏幕.get_width() - 副标题文本.get_width()) // 2, 120)
        屏幕.blit(副标题文本, 副标题位置)
        
        # 绘制所有组件
        super().绘制(屏幕) 