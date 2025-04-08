#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

class GUI界面(object):
    """GUI界面基类，所有具体界面都将继承此类"""
    
    def __init__(self, 名称):
        """初始化界面
        
        参数:
            名称(str): 界面名称
        """
        self.名称 = 名称
        self.管理器 = None  # 将由管理器在注册时设置
        self.是否初始化 = False
        
    def 初始化(self):
        """初始化界面，只会被调用一次"""
        if not self.是否初始化:
            self._初始化实现()
            self.是否初始化 = True
        
    def _初始化实现(self):
        """初始化界面的具体实现，子类需要重写此方法"""
        pass
        
    def 准备(self, 参数=None):
        """准备界面以供显示，每次切换到此界面时调用
        
        参数:
            参数(dict): 传递给界面的参数
        """
        # 确保界面已初始化
        self.初始化()
        # 调用具体实现
        self._准备实现(参数)
        
    def _准备实现(self, 参数=None):
        """准备界面的具体实现，子类需要重写此方法"""
        pass
        
    def 更新(self):
        """更新界面，每帧调用一次"""
        self._更新实现()
        
    def _更新实现(self):
        """更新界面的具体实现，子类需要重写此方法"""
        pass
        
    def 处理事件(self, 事件):
        """处理输入事件
        
        参数:
            事件: pygame事件对象
        """
        self._处理事件实现(事件)
        
    def _处理事件实现(self, 事件):
        """处理事件的具体实现，子类需要重写此方法"""
        pass
        
    def 绘制到表面(self, 表面):
        """将界面绘制到指定表面
        
        参数:
            表面: pygame Surface对象
        """
        self._绘制到表面实现(表面)
        
    def _绘制到表面实现(self, 表面):
        """绘制到表面的具体实现，子类需要重写此方法"""
        pass
        
    def 切换完成(self):
        """当切换到此界面的动画完成时调用"""
        self._切换完成实现()
        
    def _切换完成实现(self):
        """切换完成的具体实现，子类需要重写此方法"""
        pass
        
    def 关闭(self):
        """当界面关闭时调用"""
        self._关闭实现()
        
    def _关闭实现(self):
        """关闭界面的具体实现，子类需要重写此方法"""
        pass 