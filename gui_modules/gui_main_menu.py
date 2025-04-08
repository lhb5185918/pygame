#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import sys
from typing import Any, Optional

from gui_modules.gui_base import GUI界面

class 主菜单界面(GUI界面):
    """游戏主菜单界面"""
    
    def __init__(self, 背景路径: str = "picture/back_ground_picture.png"):
        """初始化主菜单界面
        
        参数:
            背景路径: 背景图片路径
        """
        super().__init__("主菜单")
        self.背景路径 = 背景路径
        self.背景 = None
        self.标题字体大小 = 48
        self.按钮字体大小 = 32
    
    def 初始化(self):
        """初始化界面资源"""
        if self.已初始化:
            return
            
        super().初始化()
        
        # 加载背景图片
        try:
            self.背景 = pygame.image.load(self.背景路径).convert_alpha()
            self.背景 = pygame.transform.scale(self.背景, self.主缓冲区.get_size())
        except Exception as e:
            print(f"无法加载背景图片: {e}")
            self.背景 = None
    
    def 准备(self, 参数: Any = None):
        """准备界面显示"""
        super().准备(参数)
        
        # 清除之前的按钮
        self.按钮列表.clear()
        
        # 绘制背景
        self._绘制背景()
        
        # 创建按钮
        屏幕宽度, 屏幕高度 = self.主缓冲区.get_size()
        按钮宽度, 按钮高度 = 300, 60
        按钮间距 = 20
        起始Y = 屏幕高度 // 2 - 100
        
        # 开始游戏按钮
        开始按钮矩形 = pygame.Rect(
            屏幕宽度 // 2 - 按钮宽度 // 2,
            起始Y,
            按钮宽度,
            按钮高度
        )
        self.创建按钮(开始按钮矩形, "开始游戏", self._开始游戏, 
                    (50, 120, 220), (70, 150, 250))
        
        # 加载游戏按钮
        加载按钮矩形 = pygame.Rect(
            屏幕宽度 // 2 - 按钮宽度 // 2,
            起始Y + 按钮高度 + 按钮间距,
            按钮宽度,
            按钮高度
        )
        self.创建按钮(加载按钮矩形, "加载游戏", self._加载游戏,
                    (50, 120, 220), (70, 150, 250))
        
        # 设置按钮
        设置按钮矩形 = pygame.Rect(
            屏幕宽度 // 2 - 按钮宽度 // 2,
            起始Y + (按钮高度 + 按钮间距) * 2,
            按钮宽度,
            按钮高度
        )
        self.创建按钮(设置按钮矩形, "设置", self._打开设置,
                    (50, 120, 220), (70, 150, 250))
        
        # 退出游戏按钮
        退出按钮矩形 = pygame.Rect(
            屏幕宽度 // 2 - 按钮宽度 // 2,
            起始Y + (按钮高度 + 按钮间距) * 3,
            按钮宽度,
            按钮高度
        )
        self.创建按钮(退出按钮矩形, "退出游戏", self._退出游戏,
                    (220, 50, 50), (250, 70, 70))
        
        # 重新绘制所有元素
        self._绘制所有元素()
    
    def 处理事件(self, 事件):
        """处理pygame事件"""
        super().处理事件(事件)
    
    def 更新(self):
        """更新界面逻辑"""
        # 重新绘制按钮以更新悬停状态
        self._绘制按钮区域()
    
    def _绘制背景(self):
        """绘制背景"""
        if self.背景:
            self.主缓冲区.blit(self.背景, (0, 0))
        else:
            self.清屏((240, 240, 255))
        
        # 绘制标题
        屏幕宽度 = self.主缓冲区.get_width()
        self.绘制文本("童年时光机", (屏幕宽度 // 2, 100), (0, 0, 0), 字体大小=self.标题字体大小, 居中=True)
        
        # 绘制版本信息
        版本信息 = "v1.0.0"
        self.绘制文本(版本信息, (10, 10), (50, 50, 50), 字体大小=16)
    
    def _绘制按钮区域(self):
        """重新绘制按钮区域"""
        # 如果有背景，先恢复背景中的按钮区域
        if self.背景:
            屏幕宽度, 屏幕高度 = self.主缓冲区.get_size()
            按钮区域 = pygame.Rect(
                屏幕宽度 // 2 - 200,
                屏幕高度 // 2 - 150,
                400,
                300
            )
            self.主缓冲区.blit(self.背景, 按钮区域, 按钮区域)
            self.脏矩形列表.append(按钮区域)
        
        # 绘制所有按钮
        self.绘制按钮()
    
    def _绘制所有元素(self):
        """绘制所有界面元素"""
        self._绘制背景()
        self.绘制按钮()
    
    def _开始游戏(self):
        """开始新游戏"""
        if self.管理器:
            self.管理器.切换到界面("角色创建")
    
    def _加载游戏(self):
        """加载游戏存档"""
        if self.管理器:
            self.管理器.切换到界面("存档列表")
    
    def _打开设置(self):
        """打开设置界面"""
        if self.管理器:
            self.管理器.切换到界面("设置")
    
    def _退出游戏(self):
        """退出游戏"""
        pygame.quit()
        sys.exit() 