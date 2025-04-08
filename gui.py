#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import sys
from gui_base import 按钮, 标签, 滑块, 复选框, 单选按钮
from gui_main import 主菜单界面
from gui_collection import 收藏品界面
from gui_attributes import 角色属性界面
from gui_settings import 设置界面

class GUI:
    """游戏GUI管理器"""
    
    def __init__(self, 宽度=800, 高度=600, 游戏引擎=None):
        """初始化游戏GUI
        
        参数:
            宽度: 窗口宽度
            高度: 窗口高度
            游戏引擎: 游戏引擎实例
        """
        pygame.init()
        pygame.display.set_caption("童年时空穿梭机")
        
        # 创建屏幕
        self.屏幕宽度 = 宽度
        self.屏幕高度 = 高度
        self.原始屏幕尺寸 = (宽度, 高度)
        self.屏幕 = pygame.display.set_mode((宽度, 高度))
        
        # 游戏引擎引用
        self.游戏引擎 = 游戏引擎
        
        # 主缓冲区 - 用于双缓冲渲染
        self.主缓冲区 = pygame.Surface((宽度, 高度))
        
        # 脏矩形列表 - 用于记录需要更新的屏幕区域
        self.脏矩形列表 = []
        
        try:
            # 加载背景图片
            self.背景图片 = pygame.image.load("picture/back_ground_picture.png").convert()
            self.背景图片 = pygame.transform.scale(self.背景图片, (宽度, 高度))
        except:
            print("无法加载背景图片，使用默认背景")
            self.背景图片 = None
        
        # 粒子系统
        self.粒子列表 = []
        self.粒子效果启用 = True
        
        # 过渡效果
        self.过渡中 = False
        self.过渡计时器 = 0
        self.过渡持续时间 = 500  # 毫秒
        self.过渡类型 = None  # 'fade_in', 'fade_out'
        self.过渡回调 = None
        
        # 消息系统
        self.消息列表 = []
        self.消息持续时间 = 3000  # 毫秒
        
        # 创建并存储界面
        self.界面 = {}
        self.当前界面 = None
        self.初始化界面()
        
        # 设置主菜单为初始界面
        self.切换界面("主菜单")
        
        # 时钟 - 用于控制帧率
        self.时钟 = pygame.time.Clock()
        self.运行中 = False
    
    def 初始化界面(self):
        """初始化所有界面"""
        self.界面 = {
            "主菜单": 主菜单界面(self),
            "收藏品": 收藏品界面(self),
            "角色属性": 角色属性界面(self),
            "设置": 设置界面(self)
        }
        
        # 初始化每个界面
        for 界面名称, 界面实例 in self.界面.items():
            界面实例.初始化()
    
    def 切换界面(self, 界面名称, 使用过渡=True):
        """切换到指定的界面
        
        参数:
            界面名称: 要切换到的界面名称
            使用过渡: 是否使用过渡效果
        """
        if 界面名称 not in self.界面:
            print(f"错误：界面 '{界面名称}' 不存在")
            return
        
        # 如果当前有界面，停用它
        if self.当前界面:
            self.当前界面.停用()
        
        if 使用过渡:
            # 使用过渡效果
            def 过渡完成回调():
                self.当前界面 = self.界面[界面名称]
                self.当前界面.激活()
                self.开始过渡('fade_in')
            
            self.开始过渡('fade_out', 过渡完成回调)
        else:
            # 不使用过渡效果，直接切换
            self.当前界面 = self.界面[界面名称]
            self.当前界面.激活()
    
    def 开始过渡(self, 类型, 完成回调=None):
        """开始一个过渡效果
        
        参数:
            类型: 过渡类型 ('fade_in', 'fade_out')
            完成回调: 过渡完成时调用的函数
        """
        self.过渡中 = True
        self.过渡计时器 = 0
        self.过渡类型 = 类型
        self.过渡回调 = 完成回调
    
    def 更新过渡(self, 时间增量):
        """更新过渡效果
        
        参数:
            时间增量: 上一帧到当前帧的时间间隔（毫秒）
        """
        if not self.过渡中:
            return
        
        self.过渡计时器 += 时间增量
        if self.过渡计时器 >= self.过渡持续时间:
            self.过渡中 = False
            if self.过渡回调:
                self.过渡回调()
                self.过渡回调 = None
    
    def 绘制过渡(self, 屏幕):
        """绘制过渡效果
        
        参数:
            屏幕: Pygame屏幕对象
        """
        if not self.过渡中:
            return
        
        进度 = self.过渡计时器 / self.过渡持续时间
        
        if self.过渡类型 == 'fade_out':
            # 淡出效果 - 从透明到黑色
            透明度 = int(255 * 进度)
        else:  # fade_in
            # 淡入效果 - 从黑色到透明
            透明度 = int(255 * (1 - 进度))
        
        # 创建一个覆盖整个屏幕的黑色半透明表面
        覆盖表面 = pygame.Surface((self.屏幕宽度, self.屏幕高度))
        覆盖表面.set_alpha(透明度)
        覆盖表面.fill((0, 0, 0))
        
        # 将覆盖表面绘制到屏幕上
        屏幕.blit(覆盖表面, (0, 0))
        
        # 记录脏矩形
        self.脏矩形列表.append(pygame.Rect(0, 0, self.屏幕宽度, self.屏幕高度))
    
    def 添加粒子(self, x, y, 颜色, 大小, 寿命, 速度x, 速度y):
        """添加一个粒子到粒子系统
        
        参数:
            x, y: 粒子位置
            颜色: 粒子颜色
            大小: 粒子大小
            寿命: 粒子寿命（毫秒）
            速度x, 速度y: 粒子速度
        """
        if not self.粒子效果启用:
            return
        
        self.粒子列表.append({
            'x': x,
            'y': y,
            '颜色': 颜色,
            '大小': 大小,
            '寿命': 寿命,
            '剩余寿命': 寿命,
            '速度x': 速度x,
            '速度y': 速度y
        })
    
    def 更新粒子(self, 时间增量):
        """更新所有粒子
        
        参数:
            时间增量: 上一帧到当前帧的时间间隔（毫秒）
        """
        if not self.粒子效果启用 or not self.粒子列表:
            return
        
        已移除 = []
        for i, 粒子 in enumerate(self.粒子列表):
            # 更新粒子位置
            粒子['x'] += 粒子['速度x'] * 时间增量 / 1000
            粒子['y'] += 粒子['速度y'] * 时间增量 / 1000
            
            # 更新粒子生命
            粒子['剩余寿命'] -= 时间增量
            
            # 如果粒子寿命已尽，标记为移除
            if 粒子['剩余寿命'] <= 0:
                已移除.append(i)
        
        # 从后向前移除粒子，以避免索引错误
        for i in reversed(已移除):
            del self.粒子列表[i]
    
    def 绘制粒子(self, 屏幕):
        """绘制所有粒子
        
        参数:
            屏幕: Pygame屏幕对象
        """
        if not self.粒子效果启用 or not self.粒子列表:
            return
        
        for 粒子 in self.粒子列表:
            # 计算粒子透明度
            透明度 = int(255 * (粒子['剩余寿命'] / 粒子['寿命']))
            颜色 = 粒子['颜色'] + (透明度,)
            
            # 绘制粒子
            位置 = (int(粒子['x']), int(粒子['y']))
            大小 = 粒子['大小']
            
            # 创建一个粒子表面
            粒子表面 = pygame.Surface((大小*2, 大小*2), pygame.SRCALPHA)
            pygame.draw.circle(粒子表面, 颜色, (大小, 大小), 大小)
            
            # 将粒子表面绘制到屏幕上
            屏幕.blit(粒子表面, (位置[0]-大小, 位置[1]-大小))
            
            # 记录脏矩形
            粒子矩形 = pygame.Rect(位置[0]-大小, 位置[1]-大小, 大小*2, 大小*2)
            self.脏矩形列表.append(粒子矩形)
    
    def 显示消息(self, 文本, 持续时间=None):
        """显示一条消息
        
        参数:
            文本: 消息文本
            持续时间: 消息显示时间（毫秒），None表示使用默认时间
        """
        if 持续时间 is None:
            持续时间 = self.消息持续时间
        
        self.消息列表.append({
            '文本': 文本,
            '剩余时间': 持续时间,
            '字体': pygame.font.Font(None, 24)
        })
    
    def 更新消息(self, 时间增量):
        """更新所有消息
        
        参数:
            时间增量: 上一帧到当前帧的时间间隔（毫秒）
        """
        if not self.消息列表:
            return
        
        已移除 = []
        for i, 消息 in enumerate(self.消息列表):
            消息['剩余时间'] -= 时间增量
            if 消息['剩余时间'] <= 0:
                已移除.append(i)
        
        # 从后向前移除消息，以避免索引错误
        for i in reversed(已移除):
            del self.消息列表[i]
    
    def 绘制消息(self, 屏幕):
        """绘制所有消息
        
        参数:
            屏幕: Pygame屏幕对象
        """
        if not self.消息列表:
            return
        
        y位置 = 10
        for 消息 in self.消息列表:
            # 计算消息透明度
            透明度 = min(255, int(255 * 消息['剩余时间'] / 1000))
            if 透明度 <= 0:
                continue
            
            # 渲染消息文本
            文本渲染 = 消息['字体'].render(消息['文本'], True, (255, 255, 255))
            文本渲染.set_alpha(透明度)
            
            # 计算消息位置
            x位置 = (self.屏幕宽度 - 文本渲染.get_width()) // 2
            
            # 绘制消息背景
            背景矩形 = pygame.Rect(x位置 - 10, y位置 - 5, 文本渲染.get_width() + 20, 文本渲染.get_height() + 10)
            背景表面 = pygame.Surface((背景矩形.width, 背景矩形.height))
            背景表面.set_alpha(min(200, 透明度))
            背景表面.fill((0, 0, 0))
            屏幕.blit(背景表面, 背景矩形)
            
            # 绘制消息文本
            屏幕.blit(文本渲染, (x位置, y位置))
            
            # 记录脏矩形
            self.脏矩形列表.append(背景矩形)
            
            y位置 += 文本渲染.get_height() + 15
    
    def 清屏(self):
        """清空屏幕并绘制背景"""
        # 清空主缓冲区
        if self.背景图片:
            self.主缓冲区.blit(self.背景图片, (0, 0))
        else:
            self.主缓冲区.fill((30, 30, 50))
        
        # 整个屏幕需要更新
        self.脏矩形列表.append(pygame.Rect(0, 0, self.屏幕宽度, self.屏幕高度))
    
    def 创建按钮(self, x, y, 宽度, 高度, 文本, 点击回调=None):
        """创建一个按钮
        
        参数:
            x, y: 按钮位置
            宽度, 高度: 按钮尺寸
            文本: 按钮文本
            点击回调: 点击按钮时调用的函数
        
        返回:
            按钮实例
        """
        return 按钮(x, y, 宽度, 高度, 文本, 点击回调)
    
    def 创建标签(self, x, y, 文本, 字体大小=28, 颜色=(255, 255, 255)):
        """创建一个文本标签
        
        参数:
            x, y: 标签位置
            文本: 标签文本
            字体大小: 字体大小
            颜色: 文本颜色
        
        返回:
            标签实例
        """
        return 标签(x, y, 文本, 字体大小, 颜色)
    
    def 创建滑块(self, x, y, 宽度, 高度, 值, 最小值, 最大值, 变化回调=None):
        """创建一个滑块
        
        参数:
            x, y: 滑块位置
            宽度, 高度: 滑块尺寸
            值: 当前值
            最小值: 最小值
            最大值: 最大值
            变化回调: 值变化时调用的函数
        
        返回:
            滑块实例
        """
        return 滑块(x, y, 宽度, 高度, 值, 最小值, 最大值, 变化回调)
    
    def 创建复选框(self, x, y, 文本, 选中=False, 变化回调=None):
        """创建一个复选框
        
        参数:
            x, y: 复选框位置
            文本: 复选框标签文本
            选中: 是否选中
            变化回调: 状态变化时调用的函数
        
        返回:
            复选框实例
        """
        return 复选框(x, y, 文本, 选中, 变化回调)
    
    def 创建单选按钮(self, x, y, 文本, 组名, 选中=False, 变化回调=None):
        """创建一个单选按钮
        
        参数:
            x, y: 单选按钮位置
            文本: 单选按钮标签文本
            组名: 单选按钮组名
            选中: 是否选中
            变化回调: 状态变化时调用的函数
        
        返回:
            单选按钮实例
        """
        return 单选按钮(x, y, 文本, 组名, 选中, 变化回调)
    
    def 绘制文本(self, 屏幕, 文本, x, y, 字体大小=28, 颜色=(255, 255, 255), 对齐="左"):
        """在屏幕上绘制文本
        
        参数:
            屏幕: Pygame屏幕对象
            文本: 要绘制的文本
            x, y: 文本位置
            字体大小: 字体大小
            颜色: 文本颜色
            对齐: 对齐方式 ("左", "中", "右")
        """
        字体 = pygame.font.Font(None, 字体大小)
        文本渲染 = 字体.render(文本, True, 颜色)
        
        if 对齐 == "中":
            x = x - 文本渲染.get_width() // 2
        elif 对齐 == "右":
            x = x - 文本渲染.get_width()
        
        屏幕.blit(文本渲染, (x, y))
        
        # 记录脏矩形
        文本矩形 = pygame.Rect(x, y, 文本渲染.get_width(), 文本渲染.get_height())
        self.脏矩形列表.append(文本矩形)
    
    def 进入全屏(self):
        """切换到全屏模式"""
        self.屏幕 = pygame.display.set_mode(self.原始屏幕尺寸, pygame.FULLSCREEN)
    
    def 退出全屏(self):
        """退出全屏模式"""
        self.屏幕 = pygame.display.set_mode(self.原始屏幕尺寸)
    
    def 处理事件(self):
        """处理所有Pygame事件
        
        返回:
            布尔值，False表示应该退出游戏
        """
        for 事件 in pygame.event.get():
            if 事件.type == pygame.QUIT:
                return False
            
            # 处理按键事件
            if 事件.type == pygame.KEYDOWN:
                if 事件.key == pygame.K_ESCAPE:
                    return False
            
            # 将事件传递给当前界面
            if self.当前界面:
                self.当前界面.处理事件(事件)
        
        return True
    
    def 更新(self, 时间增量):
        """更新GUI状态
        
        参数:
            时间增量: 上一帧到当前帧的时间间隔（毫秒）
        """
        # 更新当前界面
        if self.当前界面:
            self.当前界面.更新(时间增量)
        
        # 更新过渡效果
        self.更新过渡(时间增量)
        
        # 更新粒子
        self.更新粒子(时间增量)
        
        # 更新消息
        self.更新消息(时间增量)
    
    def 绘制(self):
        """绘制GUI到屏幕"""
        # 清屏并绘制背景
        self.清屏()
        
        # 绘制当前界面
        if self.当前界面:
            self.当前界面.绘制(self.主缓冲区)
        
        # 绘制粒子
        self.绘制粒子(self.主缓冲区)
        
        # 绘制消息
        self.绘制消息(self.主缓冲区)
        
        # 绘制过渡效果
        self.绘制过渡(self.主缓冲区)
        
        # 将主缓冲区内容复制到屏幕上
        # 使用脏矩形更新而不是全屏更新
        if self.脏矩形列表:
            # 将主缓冲区的内容按照脏矩形列表更新到屏幕上
            for 矩形 in self.脏矩形列表:
                self.屏幕.blit(self.主缓冲区, 矩形, 矩形)
            
            # 更新显示
            pygame.display.update(self.脏矩形列表)
            
            # 清空脏矩形列表
            self.脏矩形列表.clear()
        else:
            # 如果没有脏矩形，则更新整个屏幕
            self.屏幕.blit(self.主缓冲区, (0, 0))
            pygame.display.flip()
    
    def 运行(self):
        """运行GUI主循环"""
        self.运行中 = True
        最后时间 = pygame.time.get_ticks()
        
        while self.运行中:
            # 计算时间增量
            当前时间 = pygame.time.get_ticks()
            时间增量 = 当前时间 - 最后时间
            最后时间 = 当前时间
            
            # 限制帧率
            self.时钟.tick(60)
            
            # 处理事件
            self.运行中 = self.处理事件()
            
            # 更新GUI
            self.更新(时间增量)
            
            # 绘制GUI
            self.绘制()
        
        # 清理并退出
        pygame.quit()
    
    def 退出(self):
        """退出GUI"""
        self.运行中 = False

def 创建图形界面():
    """创建图形界面实例
    
    返回:
        图形界面: 界面实例
    """
    return 图形界面() 