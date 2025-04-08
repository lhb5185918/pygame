#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import sys
import os
import random
import math
from typing import Any, List, Dict, Tuple, Optional, Callable

class GUI界面:
    """GUI界面基类，所有具体界面都应继承此类"""
    
    def __init__(self, 名称: str):
        """初始化GUI界面
        
        参数:
            名称: 界面的唯一标识名称
        """
        self.名称 = 名称
        self.管理器 = None
        self.已初始化 = False
        self.按钮列表: List[Dict] = []
        self.脏矩形列表: List[pygame.Rect] = []
        self.主缓冲区: Optional[pygame.Surface] = None
        self.字体缓存: Dict[Tuple[str, int], pygame.font.Font] = {}
    
    def 设置管理器(self, 管理器):
        """设置界面管理器
        
        参数:
            管理器: 界面管理器实例
        """
        self.管理器 = 管理器
    
    def 初始化(self):
        """初始化界面资源，只会被调用一次"""
        if self.已初始化:
            return
            
        # 创建主缓冲区
        if self.管理器:
            self.主缓冲区 = pygame.Surface(self.管理器.屏幕.get_size()).convert_alpha()
        
        self.已初始化 = True
    
    def 准备(self, 参数: Any = None):
        """准备界面显示，每次界面被切换到时调用
        
        参数:
            参数: 切换到此界面时传递的参数
        """
        self.脏矩形列表.clear()
        # 标记整个屏幕为脏矩形，需要完全重绘
        if self.主缓冲区:
            self.脏矩形列表.append(self.主缓冲区.get_rect())
    
    def 处理事件(self, 事件):
        """处理pygame事件
        
        参数:
            事件: pygame事件对象
        """
        # 处理按钮点击
        if 事件.type == pygame.MOUSEBUTTONDOWN and 事件.button == 1:
            self._处理按钮点击(事件.pos)
    
    def 更新(self):
        """更新界面逻辑，每帧调用"""
        pass
    
    def 绘制到表面(self, 表面: pygame.Surface):
        """将界面绘制到指定表面上
        
        参数:
            表面: 目标pygame表面
        """
        # 只更新脏矩形区域
        for 矩形 in self.脏矩形列表:
            表面.blit(self.主缓冲区, 矩形, 矩形)
        
        # 清除脏矩形列表
        self.脏矩形列表.clear()
    
    def 关闭(self):
        """关闭界面，释放资源"""
        pass
    
    def 创建按钮(self, 矩形: pygame.Rect, 文本: str, 回调: Callable, 
               颜色: Tuple[int, int, int] = (100, 100, 100),
               悬停颜色: Tuple[int, int, int] = (150, 150, 150),
               文本颜色: Tuple[int, int, int] = (255, 255, 255),
               字体大小: int = 24):
        """创建一个界面按钮
        
        参数:
            矩形: 按钮的位置和大小
            文本: 按钮上的文本
            回调: 点击按钮时调用的函数
            颜色: 按钮的背景颜色
            悬停颜色: 鼠标悬停时按钮的颜色
            文本颜色: 按钮文本的颜色
            字体大小: 按钮文本的字体大小
        
        返回:
            按钮ID
        """
        按钮 = {
            'rect': 矩形,
            'text': 文本,
            'callback': 回调,
            'color': 颜色,
            'hover_color': 悬停颜色,
            'text_color': 文本颜色,
            'font_size': 字体大小,
            'hovered': False
        }
        
        self.按钮列表.append(按钮)
        return len(self.按钮列表) - 1
    
    def 绘制按钮(self):
        """绘制所有按钮"""
        for 按钮 in self.按钮列表:
            # 检查鼠标是否悬停在按钮上
            鼠标位置 = pygame.mouse.get_pos()
            按钮['hovered'] = 按钮['rect'].collidepoint(鼠标位置)
            
            # 选择按钮颜色
            颜色 = 按钮['hover_color'] if 按钮['hovered'] else 按钮['color']
            
            # 绘制按钮背景
            pygame.draw.rect(self.主缓冲区, 颜色, 按钮['rect'])
            pygame.draw.rect(self.主缓冲区, (0, 0, 0), 按钮['rect'], 2)  # 边框
            
            # 绘制按钮文本
            字体 = self._获取字体('simhei', 按钮['font_size'])
            文本表面 = 字体.render(按钮['text'], True, 按钮['text_color'])
            文本位置 = 文本表面.get_rect(center=按钮['rect'].center)
            self.主缓冲区.blit(文本表面, 文本位置)
            
            # 添加到脏矩形列表
            self.脏矩形列表.append(按钮['rect'])
    
    def 绘制文本(self, 文本: str, 位置: Tuple[int, int], 颜色: Tuple[int, int, int] = (0, 0, 0), 
               字体名: str = 'simhei', 字体大小: int = 24, 居中: bool = False):
        """在界面上绘制文本
        
        参数:
            文本: 要绘制的文本
            位置: 文本位置 (x, y)
            颜色: 文本颜色
            字体名: 字体名称
            字体大小: 字体大小
            居中: 是否居中对齐，若为True，则位置代表文本中心点
        
        返回:
            文本的矩形区域
        """
        字体 = self._获取字体(字体名, 字体大小)
        文本表面 = 字体.render(文本, True, 颜色)
        
        if 居中:
            文本位置 = 文本表面.get_rect(center=位置)
        else:
            文本位置 = 文本表面.get_rect(topleft=位置)
        
        self.主缓冲区.blit(文本表面, 文本位置)
        
        # 添加到脏矩形列表
        self.脏矩形列表.append(文本位置)
        
        return 文本位置
    
    def 清屏(self, 颜色: Tuple[int, int, int] = (255, 255, 255, 255)):
        """清空界面
        
        参数:
            颜色: 填充颜色
        """
        if self.主缓冲区:
            self.主缓冲区.fill(颜色)
            # 将整个表面添加到脏矩形列表
            self.脏矩形列表.append(self.主缓冲区.get_rect())
    
    def _处理按钮点击(self, 位置):
        """处理按钮点击
        
        参数:
            位置: 鼠标点击位置
        """
        for 按钮 in self.按钮列表:
            if 按钮['rect'].collidepoint(位置):
                按钮['callback']()
                break
    
    def _获取字体(self, 字体名: str, 字体大小: int) -> pygame.font.Font:
        """获取字体对象，使用缓存提高性能
        
        参数:
            字体名: 字体名称
            字体大小: 字体大小
        
        返回:
            字体对象
        """
        字体键 = (字体名, 字体大小)
        
        if 字体键 not in self.字体缓存:
            try:
                self.字体缓存[字体键] = pygame.font.SysFont(字体名, 字体大小)
            except:
                self.字体缓存[字体键] = pygame.font.Font(None, 字体大小)
        
        return self.字体缓存[字体键]

class GUI基础类:
    """基于pygame的图形界面基础类，提供基本绘制功能"""

    def __init__(self, 屏幕宽度=800, 屏幕高度=600, 标题="九零后时光机"):
        """初始化图形界面基础类
        
        参数:
            屏幕宽度(int): 屏幕宽度
            屏幕高度(int): 屏幕高度
            标题(str): 游戏标题
        """
        # 初始化pygame
        pygame.init()
        pygame.display.set_caption(标题)
        
        # 设置屏幕尺寸
        self.屏幕宽度 = 屏幕宽度
        self.屏幕高度 = 屏幕高度
        self.屏幕 = pygame.display.set_mode((self.屏幕宽度, self.屏幕高度))
        
        # 创建主缓冲区表面（用于双缓冲）
        self.主缓冲区 = pygame.Surface((self.屏幕宽度, self.屏幕高度))
        
        # 初始化脏矩形列表（用于追踪需要更新的区域）
        self.脏矩形列表 = []
        
        # 加载背景图片
        try:
            self.背景图片 = pygame.image.load("picture/back_ground_picture.png")
            self.背景图片 = pygame.transform.scale(self.背景图片, (self.屏幕宽度, self.屏幕高度))
        except Exception as e:
            print(f"无法加载背景图片：{e}，将使用默认背景")
            self.背景图片 = None
        
        # 设置颜色
        self.背景色 = (25, 30, 40)  # 更深的深灰色背景
        self.文本色 = (245, 245, 245)  # 浅白色文本
        self.标题色 = (114, 184, 240)  # 淡蓝色标题
        self.按钮色 = (70, 130, 190)  # 蓝色按钮
        self.按钮悬停色 = (95, 155, 215)  # 按钮悬停颜色
        self.高亮色 = (255, 152, 0)  # 橙色高亮
        self.属性栏颜色 = (114, 184, 240)  # 属性栏颜色
        self.属性栏边框色 = (150, 200, 255)  # 属性栏边框颜色
        
        # 加载字体
        pygame.font.init()
        self.标题字体 = pygame.font.SysFont('simhei', 42, bold=True)
        self.正文字体 = pygame.font.SysFont('simhei', 24)
        self.小字体 = pygame.font.SysFont('simhei', 18)
        
        # 创建背景元素
        self.背景粒子 = []
        for i in range(30):  # 减少粒子数量，因为有背景图片
            self.背景粒子.append({
                'x': random.randint(0, self.屏幕宽度),
                'y': random.randint(0, self.屏幕高度),
                'size': random.randint(1, 3),
                'speed': random.uniform(0.1, 0.5),
                'color': (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255), random.randint(50, 120))
            })
        
        # 游戏时钟
        self.时钟 = pygame.time.Clock()
        self.帧计数 = 0
        
        # 当前界面状态
        self.当前界面名称 = None
        
        # 按钮列表
        self.按钮列表 = []
        
        # 消息
        self.消息 = ""
        self.消息计时器 = 0
        
    def 清屏(self):
        """清除屏幕内容并绘制背景图片"""
        # 绘制背景图片到主缓冲区而不是直接到屏幕
        if self.背景图片:
            self.主缓冲区.blit(self.背景图片, (0, 0))
        else:
            # 如果没有背景图片，使用纯色背景
            self.主缓冲区.fill(self.背景色)
        
        # 绘制少量半透明粒子作为装饰
        self.帧计数 += 1
        for 粒子 in self.背景粒子:
            # 移动粒子
            粒子['y'] += 粒子['speed']
            if 粒子['y'] > self.屏幕高度:
                粒子['y'] = 0
                粒子['x'] = random.randint(0, self.屏幕宽度)
            
            # 绘制半透明粒子
            size = 粒子['size']
            x, y = int(粒子['x']), int(粒子['y'])
            intensity = (math.sin(self.帧计数 * 0.05 + x * 0.1) + 1) * 0.3 + 0.4
            
            # 创建一个带透明度的表面
            particle_surface = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
            color = list(粒子['color'])
            if len(color) == 3:  # 如果没有透明度，添加透明度
                color.append(100)  # 半透明
            pygame.draw.circle(particle_surface, color, (size, size), size)
            
            # 记录脏矩形
            粒子矩形 = pygame.Rect(x-size, y-size, size*2, size*2)
            self.脏矩形列表.append(粒子矩形)
            
            # 绘制到主缓冲区
            self.主缓冲区.blit(particle_surface, (x-size, y-size))
    
    def 绘制文本(self, 文本, x, y, 颜色=None, 字体=None, 居中=False, 阴影=False):
        """在屏幕上绘制文本，可选是否有阴影效果
        
        参数:
            文本(str): 要显示的文本
            x(int): x坐标
            y(int): y坐标
            颜色(tuple): RGB颜色元组
            字体: pygame字体对象
            居中(bool): 是否居中显示
            阴影(bool): 是否添加阴影效果
        
        返回:
            pygame.Rect: 文本所占区域的矩形，用于脏矩形跟踪
        """
        if 颜色 is None:
            颜色 = self.文本色
        if 字体 is None:
            字体 = self.正文字体
        
        # 绘制主文本并获取其矩形区域
        文本渲染 = 字体.render(文本, True, 颜色)
        文本矩形 = 文本渲染.get_rect()
        
        if 居中:
            文本矩形.center = (x, y)
        else:
            文本矩形.topleft = (x, y)
        
        # 如果需要阴影效果
        if 阴影:
            阴影颜色 = (30, 30, 30)
            阴影文本 = 字体.render(文本, True, 阴影颜色)
            阴影矩形 = 文本矩形.copy()
            阴影矩形.x += 2
            阴影矩形.y += 2
            self.主缓冲区.blit(阴影文本, 阴影矩形)
            
            # 扩大脏区域以包含阴影
            文本矩形.union_ip(阴影矩形)
        
        # 绘制到主缓冲区
        self.主缓冲区.blit(文本渲染, 文本矩形)
        
        # 记录脏矩形
        self.脏矩形列表.append(文本矩形)
        
        return 文本矩形
        
    def 绘制按钮(self, 文本, x, y, 宽度, 高度, 操作=None, 参数=None, 高亮=False):
        """绘制可点击按钮，带有视觉效果
        
        参数:
            文本(str): 按钮文本
            x(int): x坐标
            y(int): y坐标
            宽度(int): 按钮宽度
            高度(int): 按钮高度
            操作: 点击执行的函数
            参数: 传递给操作函数的参数
            高亮(bool): 是否高亮显示
            
        返回:
            pygame.Rect: 按钮的矩形区域
        """
        鼠标位置 = pygame.mouse.get_pos()
        按钮矩形 = pygame.Rect(x, y, 宽度, 高度)
        
        # 检查鼠标是否悬停在按钮上
        悬停 = 按钮矩形.collidepoint(鼠标位置)
        
        # 创建按钮计算区域的扩展矩形（包含阴影）
        扩展按钮矩形 = 按钮矩形.copy()
        扩展按钮矩形.inflate_ip(10, 10)  # 扩大区域以包含阴影和光晕效果
        
        # 记录脏矩形
        self.脏矩形列表.append(扩展按钮矩形)
        
        # 绘制按钮阴影
        阴影矩形 = pygame.Rect(x+3, y+3, 宽度, 高度)
        pygame.draw.rect(self.主缓冲区, (20, 20, 20), 阴影矩形, border_radius=8)
        
        # 绘制按钮主体
        if 高亮:
            按钮颜色 = self.高亮色
        elif 悬停:
            按钮颜色 = self.按钮悬停色
            # 绘制悬停时的光晕效果
            扩展矩形 = pygame.Rect(x-2, y-2, 宽度+4, 高度+4)
            pygame.draw.rect(self.主缓冲区, (255, 255, 255, 30), 扩展矩形, border_radius=10, width=2)
        else:
            按钮颜色 = self.按钮色
        
        pygame.draw.rect(self.主缓冲区, 按钮颜色, 按钮矩形, border_radius=8)
        
        # 添加内部光泽效果
        光泽高度 = 高度 // 3
        光泽矩形 = pygame.Rect(x+4, y+4, 宽度-8, 光泽高度)
        渐变色 = (min(255, 按钮颜色[0] + 30), min(255, 按钮颜色[1] + 30), min(255, 按钮颜色[2] + 30), 90)
        渐变表面 = pygame.Surface((宽度-8, 光泽高度), pygame.SRCALPHA)
        渐变表面.fill(渐变色)
        self.主缓冲区.blit(渐变表面, 光泽矩形)
        
        # 绘制按钮文本（带阴影）
        按钮文本 = self.正文字体.render(文本, True, (20, 20, 20))
        文本矩形 = 按钮文本.get_rect(center=(按钮矩形.centerx+1, 按钮矩形.centery+1))
        self.主缓冲区.blit(按钮文本, 文本矩形)
        
        按钮文本 = self.正文字体.render(文本, True, (255, 255, 255))
        文本矩形 = 按钮文本.get_rect(center=按钮矩形.center)
        self.主缓冲区.blit(按钮文本, 文本矩形)
        
        # 存储按钮信息
        按钮信息 = {
            "矩形": 按钮矩形,
            "文本": 文本,
            "操作": 操作,
            "参数": 参数
        }
        self.按钮列表.append(按钮信息)
        
        return 按钮矩形
        
    def 显示标题(self):
        """显示游戏标题和装饰元素"""
        # 绘制标题栏背景
        标题背景 = pygame.Rect(0, 0, self.屏幕宽度, 90)
        pygame.draw.rect(self.主缓冲区, (30, 35, 45), 标题背景)
        
        # 将标题区域添加到脏矩形列表
        self.脏矩形列表.append(标题背景)
        
        # 绘制标题下方的装饰线
        pygame.draw.line(self.主缓冲区, (80, 120, 180), (0, 90), (self.屏幕宽度, 90), 2)
        
        # 绘制动态标题文本
        波浪偏移 = math.sin(self.帧计数 * 0.05) * 3
        self.绘制文本("九零后时光机", self.屏幕宽度//2, 45 + 波浪偏移, self.标题色, self.标题字体, True, True)
        
        # 在标题两侧添加装饰元素
        左边距 = self.屏幕宽度//2 - 180
        右边距 = self.屏幕宽度//2 + 180
        
        # 绘制左侧装饰
        pygame.draw.circle(self.主缓冲区, (100, 150, 220), (左边距, 45), 8)
        pygame.draw.line(self.主缓冲区, (100, 150, 220), (左边距 - 40, 45), (左边距 - 10, 45), 2)
        
        # 绘制右侧装饰
        pygame.draw.circle(self.主缓冲区, (100, 150, 220), (右边距, 45), 8)
        pygame.draw.line(self.主缓冲区, (100, 150, 220), (右边距 + 10, 45), (右边距 + 40, 45), 2)

    def 显示文本(self, 文本, 延迟=0):
        """显示文本，可设置延迟，带有渐变效果
        
        参数:
            文本(str): 要显示的文本
            延迟(float): 显示后的延迟时间（秒）
        """
        # 创建半透明消息条
        消息背景 = pygame.Rect(10, self.屏幕高度 - 60, self.屏幕宽度 - 20, 50)
        消息表面 = pygame.Surface((self.屏幕宽度 - 20, 50), pygame.SRCALPHA)
        消息表面.fill((30, 35, 40, 200))
        self.主缓冲区.blit(消息表面, 消息背景)
        pygame.draw.rect(self.主缓冲区, (70, 100, 150), 消息背景, border_radius=10, width=2)
        
        # 记录脏矩形
        self.脏矩形列表.append(消息背景)
        
        self.消息 = 文本
        self.消息计时器 = pygame.time.get_ticks()
        self.绘制文本(文本, self.屏幕宽度//2, self.屏幕高度 - 35, self.高亮色, self.正文字体, True)
        
        # 将主缓冲区内容更新到屏幕
        self.屏幕.blit(self.主缓冲区, (0, 0))
        pygame.display.update(self.脏矩形列表)
        
        if 延迟 > 0:
            pygame.time.wait(int(延迟 * 1000))
    
    def 清除底部区域(self):
        """清除屏幕底部区域，确保没有遮挡内容"""
        底部区域 = pygame.Rect(0, self.屏幕高度 - 100, self.屏幕宽度, 100)
        
        # 使用背景图片或颜色填充底部区域
        if self.背景图片:
            区域背景 = self.背景图片.subsurface(底部区域)
            self.主缓冲区.blit(区域背景, 底部区域)
        else:
            pygame.draw.rect(self.主缓冲区, self.背景色, 底部区域)
        
        # 将区域添加到脏矩形列表
        self.脏矩形列表.append(底部区域)
    
    def 等待按键(self, 提示="点击继续"):
        """等待用户按键继续
        
        参数:
            提示(str): 提示文本
        """
        按钮矩形 = self.绘制按钮(提示, self.屏幕宽度//2 - 100, self.屏幕高度 - 80, 200, 40, None, None)
        
        # 将主缓冲区内容更新到屏幕
        self.屏幕.blit(self.主缓冲区, (0, 0))
        pygame.display.update(self.脏矩形列表)
        
        等待中 = True
        while 等待中:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    等待中 = False
            
            self.时钟.tick(30)
    
    def 处理事件(self):
        """处理pygame事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # 左键点击
                for 按钮 in self.按钮列表:
                    if 按钮["矩形"].collidepoint(event.pos):
                        # 返回被点击的按钮信息
                        return 按钮
        
        return None
    
    def 更新(self):
        """更新界面状态（由子类实现具体内容）"""
        # 增加帧计数器
        self.帧计数 += 1
        
        # 处理消息超时
        当前时间 = pygame.time.get_ticks()
        if self.消息 and 当前时间 - self.消息计时器 > 3000:
            self.消息 = ""
            # 确保消息区域被标记为脏矩形，以便重绘
            消息区域 = pygame.Rect(10, self.屏幕高度 - 60, self.屏幕宽度 - 20, 50)
            self.脏矩形列表.append(消息区域)
            # 重绘该区域（使用背景）
            if self.背景图片:
                区域背景 = self.背景图片.subsurface(消息区域)
                self.主缓冲区.blit(区域背景, 消息区域)
                
        # 将主缓冲区内容更新到屏幕
        self.屏幕.blit(self.主缓冲区, (0, 0))
        
        # 仅更新脏矩形区域，而不是整个屏幕
        if self.脏矩形列表:
            pygame.display.update(self.脏矩形列表)
        else:
            # 如果没有脏矩形，则更新整个屏幕（首次渲染或全屏更新）
            pygame.display.flip()
        
        # 清空脏矩形列表
        self.脏矩形列表 = [] 