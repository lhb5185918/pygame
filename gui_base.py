#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

class 界面基类:
    """界面基类，所有界面类的父类"""
    
    def __init__(self, gui):
        """初始化界面基类
        
        参数:
            gui: GUI管理器实例
        """
        self.gui = gui
        self.组件列表 = []
        self.活跃 = False
    
    def 初始化(self):
        """初始化界面，子类需要重写此方法"""
        pass
    
    def 激活(self):
        """激活此界面"""
        self.活跃 = True
        self.更新组件状态()
    
    def 停用(self):
        """停用此界面"""
        self.活跃 = False
        self.更新组件状态()
    
    def 更新组件状态(self):
        """根据界面的活跃状态更新所有组件"""
        for 组件 in self.组件列表:
            组件.活跃 = self.活跃
    
    def 添加组件(self, 组件):
        """添加界面组件
        
        参数:
            组件: 要添加的界面组件
        """
        self.组件列表.append(组件)
        组件.活跃 = self.活跃
    
    def 清空组件(self):
        """清空所有界面组件"""
        self.组件列表.clear()
    
    def 处理事件(self, 事件):
        """处理Pygame事件
        
        参数:
            事件: Pygame事件对象
        返回:
            布尔值，表示事件是否被处理
        """
        if not self.活跃:
            return False
        
        # 传递事件给所有组件
        for 组件 in self.组件列表:
            if 组件.处理事件(事件):
                return True
        
        return False
    
    def 更新(self, 时间增量):
        """更新界面
        
        参数:
            时间增量: 上一帧到当前帧的时间间隔（毫秒）
        """
        if not self.活跃:
            return
        
        # 更新所有组件
        for 组件 in self.组件列表:
            组件.更新(时间增量)
    
    def 绘制(self, 屏幕):
        """绘制界面
        
        参数:
            屏幕: Pygame屏幕对象
        """
        if not self.活跃:
            return
        
        # 绘制所有组件
        for 组件 in self.组件列表:
            组件.绘制(屏幕)


class 界面组件基类:
    """界面组件基类，所有界面组件的父类"""
    
    def __init__(self, x, y, 宽度, 高度):
        """初始化界面组件基类
        
        参数:
            x, y: 组件位置
            宽度, 高度: 组件尺寸
        """
        self.x = x
        self.y = y
        self.宽度 = 宽度
        self.高度 = 高度
        self.矩形 = pygame.Rect(x, y, 宽度, 高度)
        self.活跃 = True
        self.悬停 = False
        self.点击 = False
    
    def 处理事件(self, 事件):
        """处理Pygame事件
        
        参数:
            事件: Pygame事件对象
        返回:
            布尔值，表示事件是否被处理
        """
        if not self.活跃:
            return False
        
        # 检查鼠标是否在组件上
        鼠标位置 = pygame.mouse.get_pos()
        之前悬停 = self.悬停
        self.悬停 = self.矩形.collidepoint(鼠标位置)
        
        # 处理鼠标进入和离开事件
        if not 之前悬停 and self.悬停:
            self.当鼠标进入()
        elif 之前悬停 and not self.悬停:
            self.当鼠标离开()
        
        # 处理鼠标按下事件
        if 事件.type == pygame.MOUSEBUTTONDOWN and 事件.button == 1:
            if self.悬停:
                self.点击 = True
                self.当鼠标按下()
                return True
        
        # 处理鼠标释放事件
        elif 事件.type == pygame.MOUSEBUTTONUP and 事件.button == 1:
            之前点击 = self.点击
            self.点击 = False
            if 之前点击 and self.悬停:
                self.当鼠标释放()
                return True
        
        return False
    
    def 更新(self, 时间增量):
        """更新组件
        
        参数:
            时间增量: 上一帧到当前帧的时间间隔（毫秒）
        """
        pass
    
    def 绘制(self, 屏幕):
        """绘制组件
        
        参数:
            屏幕: Pygame屏幕对象
        """
        pass
    
    def 当鼠标进入(self):
        """当鼠标进入组件时调用"""
        pass
    
    def 当鼠标离开(self):
        """当鼠标离开组件时调用"""
        pass
    
    def 当鼠标按下(self):
        """当鼠标在组件上按下时调用"""
        pass
    
    def 当鼠标释放(self):
        """当鼠标在组件上释放时调用"""
        pass


class 按钮(界面组件基类):
    """按钮组件"""
    
    def __init__(self, x, y, 宽度, 高度, 文本, 点击回调=None):
        """初始化按钮
        
        参数:
            x, y: 按钮位置
            宽度, 高度: 按钮尺寸
            文本: 按钮文本
            点击回调: 点击按钮时调用的函数
        """
        super().__init__(x, y, 宽度, 高度)
        self.文本 = 文本
        self.点击回调 = 点击回调
        self.字体 = pygame.font.Font(None, 28)
        self.文本渲染 = self.字体.render(文本, True, (255, 255, 255))
        self.文本位置 = (
            x + (宽度 - self.文本渲染.get_width()) // 2,
            y + (高度 - self.文本渲染.get_height()) // 2
        )
        self.正常颜色 = (100, 100, 180)
        self.悬停颜色 = (120, 120, 200)
        self.点击颜色 = (80, 80, 160)
        self.禁用颜色 = (70, 70, 100)
    
    def 绘制(self, 屏幕):
        """绘制按钮
        
        参数:
            屏幕: Pygame屏幕对象
        """
        if not self.活跃:
            颜色 = self.禁用颜色
        elif self.点击:
            颜色 = self.点击颜色
        elif self.悬停:
            颜色 = self.悬停颜色
        else:
            颜色 = self.正常颜色
        
        # 绘制按钮背景
        pygame.draw.rect(屏幕, 颜色, self.矩形, 0, 5)
        
        # 绘制按钮边框
        pygame.draw.rect(屏幕, (200, 200, 200), self.矩形, 2, 5)
        
        # 绘制按钮文本
        屏幕.blit(self.文本渲染, self.文本位置)
    
    def 当鼠标释放(self):
        """当鼠标在按钮上释放时调用点击回调"""
        if self.点击回调:
            self.点击回调()


class 标签(界面组件基类):
    """文本标签组件"""
    
    def __init__(self, x, y, 文本, 字体大小=28, 颜色=(255, 255, 255)):
        """初始化标签
        
        参数:
            x, y: 标签位置
            文本: 标签文本
            字体大小: 字体大小
            颜色: 文本颜色
        """
        self.字体 = pygame.font.Font(None, 字体大小)
        self.文本渲染 = self.字体.render(文本, True, 颜色)
        super().__init__(x, y, self.文本渲染.get_width(), self.文本渲染.get_height())
        self.文本 = 文本
        self.颜色 = 颜色
    
    def 绘制(self, 屏幕):
        """绘制标签
        
        参数:
            屏幕: Pygame屏幕对象
        """
        if self.活跃:
            屏幕.blit(self.文本渲染, (self.x, self.y))


class 滑块(界面组件基类):
    """滑块组件"""
    
    def __init__(self, x, y, 宽度, 高度, 值, 最小值, 最大值, 变化回调=None):
        """初始化滑块
        
        参数:
            x, y: 滑块位置
            宽度, 高度: 滑块尺寸
            值: 当前值
            最小值: 最小值
            最大值: 最大值
            变化回调: 值变化时调用的函数
        """
        super().__init__(x, y, 宽度, 高度)
        self.值 = 值
        self.最小值 = 最小值
        self.最大值 = 最大值
        self.变化回调 = 变化回调
        self.拖动中 = False
        self.滑块宽度 = 20
        self.更新滑块位置()
    
    def 更新滑块位置(self):
        """根据当前值更新滑块位置"""
        范围 = self.最大值 - self.最小值
        if 范围 == 0:
            相对位置 = 0
        else:
            相对位置 = (self.值 - self.最小值) / 范围
        
        滑块x = self.x + int((self.宽度 - self.滑块宽度) * 相对位置)
        self.滑块矩形 = pygame.Rect(滑块x, self.y, self.滑块宽度, self.高度)
    
    def 设置值(self, x位置):
        """根据x位置设置滑块值
        
        参数:
            x位置: 鼠标x坐标
        """
        相对位置 = max(0, min(1, (x位置 - self.x) / self.宽度))
        新值 = self.最小值 + 相对位置 * (self.最大值 - self.最小值)
        if 新值 != self.值:
            self.值 = 新值
            self.更新滑块位置()
            if self.变化回调:
                self.变化回调(int(self.值))
    
    def 处理事件(self, 事件):
        """处理Pygame事件
        
        参数:
            事件: Pygame事件对象
        返回:
            布尔值，表示事件是否被处理
        """
        if not self.活跃:
            return False
        
        鼠标位置 = pygame.mouse.get_pos()
        
        # 处理鼠标按下事件
        if 事件.type == pygame.MOUSEBUTTONDOWN and 事件.button == 1:
            if self.矩形.collidepoint(鼠标位置):
                self.拖动中 = True
                self.设置值(鼠标位置[0])
                return True
        
        # 处理鼠标释放事件
        elif 事件.type == pygame.MOUSEBUTTONUP and 事件.button == 1:
            if self.拖动中:
                self.拖动中 = False
                return True
        
        # 处理鼠标移动事件
        elif 事件.type == pygame.MOUSEMOTION:
            if self.拖动中:
                self.设置值(鼠标位置[0])
                return True
        
        return False
    
    def 绘制(self, 屏幕):
        """绘制滑块
        
        参数:
            屏幕: Pygame屏幕对象
        """
        if not self.活跃:
            return
        
        # 绘制滑块轨道
        pygame.draw.rect(屏幕, (50, 50, 50), self.矩形, 0, 5)
        
        # 绘制滑块已填充部分
        填充宽度 = self.滑块矩形.x - self.x + self.滑块宽度 // 2
        填充矩形 = pygame.Rect(self.x, self.y, 填充宽度, self.高度)
        pygame.draw.rect(屏幕, (100, 100, 180), 填充矩形, 0, 5)
        
        # 绘制滑块
        pygame.draw.rect(屏幕, (150, 150, 220), self.滑块矩形, 0, 5)
        pygame.draw.rect(屏幕, (200, 200, 250), self.滑块矩形, 2, 5)


class 复选框(界面组件基类):
    """复选框组件"""
    
    def __init__(self, x, y, 文本, 选中=False, 变化回调=None):
        """初始化复选框
        
        参数:
            x, y: 复选框位置
            文本: 复选框标签文本
            选中: 是否选中
            变化回调: 状态变化时调用的函数
        """
        self.字体 = pygame.font.Font(None, 28)
        self.文本渲染 = self.字体.render(文本, True, (255, 255, 255))
        self.复选框大小 = 24
        宽度 = self.复选框大小 + 10 + self.文本渲染.get_width()
        高度 = max(self.复选框大小, self.文本渲染.get_height())
        
        super().__init__(x, y, 宽度, 高度)
        self.文本 = 文本
        self.选中 = 选中
        self.变化回调 = 变化回调
        
        # 复选框矩形
        self.复选框矩形 = pygame.Rect(x, y + (高度 - self.复选框大小) // 2, 
                              self.复选框大小, self.复选框大小)
    
    def 当鼠标释放(self):
        """切换复选框状态"""
        self.选中 = not self.选中
        if self.变化回调:
            self.变化回调(self.选中)
    
    def 绘制(self, 屏幕):
        """绘制复选框
        
        参数:
            屏幕: Pygame屏幕对象
        """
        if not self.活跃:
            return
        
        # 绘制复选框
        if self.选中:
            # 选中状态绘制蓝色背景
            pygame.draw.rect(屏幕, (100, 100, 180), self.复选框矩形, 0, 3)
            
            # 绘制勾号
            内边距 = 5
            pygame.draw.line(屏幕, (255, 255, 255),
                          (self.复选框矩形.left + 内边距, self.复选框矩形.centery),
                          (self.复选框矩形.centerx, self.复选框矩形.bottom - 内边距), 2)
            pygame.draw.line(屏幕, (255, 255, 255),
                          (self.复选框矩形.centerx, self.复选框矩形.bottom - 内边距),
                          (self.复选框矩形.right - 内边距, self.复选框矩形.top + 内边距), 2)
        else:
            # 未选中状态绘制空白背景
            pygame.draw.rect(屏幕, (50, 50, 50), self.复选框矩形, 0, 3)
        
        # 绘制边框
        pygame.draw.rect(屏幕, (200, 200, 200), self.复选框矩形, 2, 3)
        
        # 绘制文本
        屏幕.blit(self.文本渲染, (self.复选框矩形.right + 10, 
                          self.y + (self.高度 - self.文本渲染.get_height()) // 2))


class 单选按钮(界面组件基类):
    """单选按钮组件"""
    
    # 用于存储每个单选组的选中状态
    组选中状态 = {}
    
    def __init__(self, x, y, 文本, 组名, 选中=False, 变化回调=None):
        """初始化单选按钮
        
        参数:
            x, y: 单选按钮位置
            文本: 单选按钮标签文本
            组名: 单选按钮组名
            选中: 是否选中
            变化回调: 状态变化时调用的函数
        """
        self.字体 = pygame.font.Font(None, 28)
        self.文本渲染 = self.字体.render(文本, True, (255, 255, 255))
        self.按钮大小 = 24
        宽度 = self.按钮大小 + 10 + self.文本渲染.get_width()
        高度 = max(self.按钮大小, self.文本渲染.get_height())
        
        super().__init__(x, y, 宽度, 高度)
        self.文本 = 文本
        self.组名 = 组名
        self.选中 = 选中
        self.变化回调 = 变化回调
        
        # 按钮矩形
        self.按钮矩形 = pygame.Rect(x, y + (高度 - self.按钮大小) // 2, 
                            self.按钮大小, self.按钮大小)
        
        # 如果初始化为选中状态，更新组选中状态
        if 选中:
            单选按钮.组选中状态[组名] = self
    
    def 当鼠标释放(self):
        """选中单选按钮"""
        if not self.选中:
            # 取消之前选中的按钮
            if self.组名 in 单选按钮.组选中状态:
                之前按钮 = 单选按钮.组选中状态[self.组名]
                之前按钮.选中 = False
            
            # 选中当前按钮
            self.选中 = True
            单选按钮.组选中状态[self.组名] = self
            
            if self.变化回调:
                self.变化回调(True)
    
    def 绘制(self, 屏幕):
        """绘制单选按钮
        
        参数:
            屏幕: Pygame屏幕对象
        """
        if not self.活跃:
            return
        
        # 绘制圆形按钮
        pygame.draw.circle(屏幕, (50, 50, 50), self.按钮矩形.center, self.按钮大小 // 2)
        pygame.draw.circle(屏幕, (200, 200, 200), self.按钮矩形.center, self.按钮大小 // 2, 2)
        
        # 如果选中，绘制内部填充
        if self.选中:
            pygame.draw.circle(屏幕, (100, 100, 180), self.按钮矩形.center, self.按钮大小 // 2 - 5)
        
        # 绘制文本
        屏幕.blit(self.文本渲染, (self.按钮矩形.right + 10, 
                          self.y + (self.高度 - self.文本渲染.get_height()) // 2)) 