#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import os
import sys
import time
import random
import math

class 图形界面:
    """基于pygame的图形界面类，提供可视化游戏体验"""

    def __init__(self, 标题="九零后时光机"):
        """初始化图形界面
        
        参数:
            标题(str): 游戏标题
        """
        # 初始化pygame
        pygame.init()
        pygame.display.set_caption(标题)
        
        # 设置屏幕尺寸
        self.屏幕宽度 = 800
        self.屏幕高度 = 600
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
        self.运行中 = True
        self.帧计数 = 0
        
        # 当前选择和界面状态
        self.当前选择 = 0
        self.当前界面 = "主菜单"
        self.玩家信息 = None
        self.消息 = ""
        self.消息计时器 = 0
        
        # 按钮和选项
        self.按钮列表 = []
        self.选项列表 = []
        
        # 回调函数
        self.回调 = None
        
        # 过渡效果变量
        self.过渡中 = False
        self.过渡计时 = 0
        self.过渡时长 = 500  # 毫秒
        
        # 初始界面
        self.清屏()
        
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
        
        # 如果有过渡动画，绘制渐变效果
        if self.过渡中:
            当前时间 = pygame.time.get_ticks()
            过渡进度 = min(1.0, (当前时间 - self.过渡计时) / self.过渡时长)
            
            # 渐变覆盖层
            覆盖层 = pygame.Surface((self.屏幕宽度, self.屏幕高度), pygame.SRCALPHA)
            覆盖层颜色 = (0, 0, 0, int(255 * (1.0 - 过渡进度)))
            覆盖层.fill(覆盖层颜色)
            self.主缓冲区.blit(覆盖层, (0, 0))
            
            # 整个屏幕都需要更新
            self.脏矩形列表.append(pygame.Rect(0, 0, self.屏幕宽度, self.屏幕高度))
            
            # 如果过渡完成
            if 过渡进度 >= 1.0:
                self.过渡中 = False
        
        # 此处不调用pygame.display.flip()，将在更新方法中统一处理
        
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
        
    def 显示收藏品(self, 收藏品列表):
        """显示玩家的收藏品，带有分类和视觉效果
        
        参数:
            收藏品列表(list): 收藏品名称列表
        """
        self.清屏()
        self.显示标题()
        
        # 创建收藏品面板背景
        面板背景 = pygame.Rect(20, 110, self.屏幕宽度 - 40, 460)
        pygame.draw.rect(self.主缓冲区, (35, 40, 50), 面板背景, border_radius=10)
        pygame.draw.rect(self.主缓冲区, (70, 100, 150), 面板背景, border_radius=10, width=2)
        
        # 记录脏矩形
        self.脏矩形列表.append(面板背景)
        
        if not 收藏品列表:
            self.绘制文本("你还没有收集到任何宝贵的童年收藏品。", self.屏幕宽度//2, 200, self.文本色, self.正文字体, True, True)
            提示文本 = "探索世界，收集90年代的珍贵物品吧！"
            self.绘制文本(提示文本, self.屏幕宽度//2, 240, self.高亮色, self.正文字体, True)
        else:
            # 绘制标题和装饰
            self.绘制文本("【童年收藏品】", self.屏幕宽度//2, 140, self.高亮色, self.正文字体, True, True)
            标题线矩形 = pygame.Rect(self.屏幕宽度//2 - 120, 155, 240, 2)
            pygame.draw.line(self.主缓冲区, self.高亮色, (self.屏幕宽度//2 - 120, 155), (self.屏幕宽度//2 + 120, 155), 2)
            self.脏矩形列表.append(标题线矩形)
            
            # 尝试对收藏品进行分类
            分类收藏品 = {
                "玩具": [],
                "卡片": [],
                "零食": [],
                "科技": [],
                "其他": []
            }
            
            # 简单分类规则
            for 收藏品 in 收藏品列表:
                if any(关键词 in 收藏品 for 关键词 in ["车", "玩具", "机器人", "模型", "积木"]):
                    分类收藏品["玩具"].append(收藏品)
                elif any(关键词 in 收藏品 for 关键词 in ["卡", "贴纸", "画片"]):
                    分类收藏品["卡片"].append(收藏品)
                elif any(关键词 in 收藏品 for 关键词 in ["糖", "饼", "食", "饮料", "零食"]):
                    分类收藏品["零食"].append(收藏品)
                elif any(关键词 in 收藏品 for 关键词 in ["电子", "游戏机", "随身听", "手机", "电脑"]):
                    分类收藏品["科技"].append(收藏品)
                else:
                    分类收藏品["其他"].append(收藏品)
            
            y = 180
            for 分类, 物品列表 in 分类收藏品.items():
                if not 物品列表:
                    continue
                    
                # 绘制分类标题
                类别图标 = "📦"
                if 分类 == "玩具":
                    类别图标 = "🧸"
                elif 分类 == "卡片":
                    类别图标 = "🃏"
                elif 分类 == "零食":
                    类别图标 = "🍬"
                elif 分类 == "科技":
                    类别图标 = "📱"
                
                self.绘制文本(f"{类别图标} {分类}:", 40, y, self.高亮色)
                y += 30
                
                # 按两列显示收藏品
                列数 = 2
                单列数量 = (len(物品列表) + 列数 - 1) // 列数
                
                for i, 收藏品 in enumerate(物品列表):
                    列索引 = i // 单列数量
                    行索引 = i % 单列数量
                    x = 60 + 列索引 * 360
                    y_pos = y + 行索引 * 25
                    
                    # 为不同年代的收藏品设置不同颜色
                    颜色 = self.文本色
                    if "90年代" in 收藏品 or "1990" in 收藏品:
                        颜色 = (180, 140, 250)  # 紫色（90年代）
                    elif "00年代" in 收藏品 or "2000" in 收藏品:
                        颜色 = (140, 180, 250)  # 蓝色（00年代）
                    
                    self.绘制文本(f"• {收藏品}", x, y_pos, 颜色)
                
                y += (单列数量 * 25) + 15
            
            # 绘制收藏进度
            总数 = sum(len(物品) for 物品 in 分类收藏品.values())
            进度文本 = f"已收集: {总数} 件珍贵物品"
            self.绘制文本(进度文本, self.屏幕宽度//2, self.屏幕高度 - 100, self.高亮色, self.正文字体, True)
        
        # 绘制返回按钮
        self.绘制按钮("返回主菜单", self.屏幕宽度//2 - 100, self.屏幕高度 - 70, 200, 50, self.显示主菜单)
        
        # 将主缓冲区内容更新到屏幕
        self.屏幕.blit(self.主缓冲区, (0, 0))
        pygame.display.update(self.脏矩形列表)
        
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
        
    def 显示属性(self, 属性字典):
        """显示玩家属性值，带有动画效果
        
        参数:
            属性字典(dict): 属性名和值的字典
        """
        self.清屏()
        self.显示标题()
        
        # 创建属性面板背景
        面板背景 = pygame.Rect(20, 110, self.屏幕宽度 - 40, 460)
        pygame.draw.rect(self.主缓冲区, (35, 40, 50), 面板背景, border_radius=10)
        pygame.draw.rect(self.主缓冲区, (70, 100, 150), 面板背景, border_radius=10, width=2)
        
        # 记录脏矩形
        self.脏矩形列表.append(面板背景)
        
        # 绘制标题和装饰
        self.绘制文本("【个人属性】", self.屏幕宽度//2, 140, self.高亮色, self.正文字体, True, True)
        
        # 绘制装饰线
        标题线矩形 = pygame.Rect(self.屏幕宽度//2 - 120, 155, 240, 2)
        pygame.draw.line(self.主缓冲区, self.高亮色, (self.屏幕宽度//2 - 120, 155), (self.屏幕宽度//2 + 120, 155), 2)
        self.脏矩形列表.append(标题线矩形)
        
        y = 180
        
        # 为每个属性创建渐变动画效果
        for i, (属性, 值) in enumerate(属性字典.items()):
            # 计算动画延迟（让每个属性按顺序显示）
            动画延迟 = i * 5
            动画进度 = min(1.0, max(0, (self.帧计数 - 动画延迟) / 20))
            
            # 绘制属性名（带图标）
            属性图标 = "📊"  # 默认图标
            if "学业" in 属性:
                属性图标 = "📚"
            elif "零花钱" in 属性:
                属性图标 = "💰"
            elif "家庭" in 属性:
                属性图标 = "👪"
            elif "健康" in 属性:
                属性图标 = "❤️"
            elif "爱国" in 属性:
                属性图标 = "🏆"
            elif "人际" in 属性:
                属性图标 = "👥"
                
            self.绘制文本(f"{属性图标} {属性}:", 40, y)
            
            # 绘制进度条背景
            进度条背景 = pygame.Rect(150, y+5, 400, 20)
            pygame.draw.rect(self.主缓冲区, (70, 70, 70), 进度条背景, border_radius=5)
            
            # 记录脏矩形
            self.脏矩形列表.append(进度条背景)
            
            # 绘制动画进度条
            显示进度 = 值 * 动画进度
            进度宽度 = 显示进度 * 4  # 0-100值映射到0-400宽度
            
            # 根据属性值确定颜色
            if 值 < 30:
                颜色 = (200, 60, 60)  # 红色（低）
            elif 值 < 60:
                颜色 = (220, 180, 60)  # 黄色（中）
            else:
                颜色 = (60, 180, 120)  # 绿色（高）
            
            进度条矩形 = pygame.Rect(150, y+5, 进度宽度, 20)
            pygame.draw.rect(self.主缓冲区, 颜色, 进度条矩形, border_radius=5)
            self.脏矩形列表.append(进度条矩形)
            
            # 添加进度条光泽效果
            光泽高度 = 8
            光泽矩形 = pygame.Rect(150, y+5, 进度宽度, 光泽高度)
            渐变色 = (min(255, 颜色[0] + 50), min(255, 颜色[1] + 50), min(255, 颜色[2] + 50), 90)
            渐变表面 = pygame.Surface((进度宽度, 光泽高度), pygame.SRCALPHA)
            渐变表面.fill(渐变色)
            self.主缓冲区.blit(渐变表面, 光泽矩形)
            
            # 绘制数值
            self.绘制文本(f"{int(显示进度)}/100", 570, y)
            
            y += 50
            
        # 绘制返回按钮
        self.绘制按钮("返回主菜单", self.屏幕宽度//2 - 100, self.屏幕高度 - 70, 200, 50, self.显示主菜单)
        
        # 将主缓冲区内容更新到屏幕
        self.屏幕.blit(self.主缓冲区, (0, 0))
        pygame.display.update(self.脏矩形列表)
        
    def 显示年代特色(self, 年份, 特色列表):
        """显示特定年份的文化特色
        
        参数:
            年份(int): 年份
            特色列表(list): 特色描述列表
        """
        self.清屏()
        self.显示标题()
        
        # 创建面板背景
        面板背景 = pygame.Rect(20, 110, self.屏幕宽度 - 40, 460)
        pygame.draw.rect(self.主缓冲区, (35, 40, 50), 面板背景, border_radius=10)
        pygame.draw.rect(self.主缓冲区, (70, 100, 150), 面板背景, border_radius=10, width=2)
        
        # 记录脏矩形
        self.脏矩形列表.append(面板背景)
        
        # 绘制年份标题
        年份文本 = f"【{年份}年的流行元素】"
        self.绘制文本(年份文本, self.屏幕宽度//2, 140, self.高亮色, self.正文字体, True, True)
        pygame.draw.line(self.主缓冲区, self.高亮色, (self.屏幕宽度//2 - 150, 155), (self.屏幕宽度//2 + 150, 155), 2)
        
        # 绘制年代背景气息描述
        年代描述 = self.获取年代描述(年份)
        if 年代描述:
            描述框 = pygame.Rect(50, 170, self.屏幕宽度 - 100, 60)
            pygame.draw.rect(self.主缓冲区, (45, 50, 60), 描述框, border_radius=8)
            
            行数 = 0
            for 行 in 年代描述.split('\n'):
                self.绘制文本(行, self.屏幕宽度//2, 185 + 行数 * 25, (200, 200, 200), self.小字体, True)
                行数 += 1
                
        # 显示特色元素
        y = 250
        for i, 特色 in enumerate(特色列表):
            # 添加简单的图标
            图标 = "🔍"
            if "游戏" in 特色 or "玩具" in 特色:
                图标 = "🎮"
            elif "电视" in 特色 or "节目" in 特色 or "播出" in 特色:
                图标 = "📺"
            elif "手机" in 特色 or "电脑" in 特色 or "网络" in 特色:
                图标 = "💻"
            elif "歌曲" in 特色 or "音乐" in 特色:
                图标 = "🎵"
            elif "流行语" in 特色 or "流行词" in 特色:
                图标 = "💬"
            
            # 为每个特色添加动画效果
            动画延迟 = i * 5
            动画进度 = min(1.0, max(0, (self.帧计数 - 动画延迟) / 15))
            
            x偏移 = (1 - 动画进度) * 50
            透明度 = int(255 * 动画进度)
            
            # 创建半透明特色项
            特色表面 = pygame.Surface((700, 40), pygame.SRCALPHA)
            pygame.draw.rect(特色表面, (60, 70, 90, 透明度), pygame.Rect(0, 0, 700, 40), border_radius=8)
            self.主缓冲区.blit(特色表面, (50 + x偏移, y - 5))
            
            self.绘制文本(f"{图标} {特色}", 70 + x偏移, y, (255, 255, 255, 透明度))
            y += 50
            
        # 绘制返回按钮
        self.绘制按钮("返回主菜单", self.屏幕宽度//2 - 100, self.屏幕高度 - 70, 200, 50, self.显示主菜单)
        
        # 将主缓冲区内容更新到屏幕
        self.屏幕.blit(self.主缓冲区, (0, 0))
        pygame.display.update(self.脏矩形列表)
        
    def 获取年代描述(self, 年份):
        """获取特定年份的背景描述
        
        参数:
            年份(int): 年份
            
        返回:
            str: 年代描述
        """
        if 1996 <= 年份 <= 2000:
            return "世纪末的中国，改革开放蓬勃发展，互联网初步进入大众视野。\n小霸王学习机、水浒卡、录像厅成为这个时代的独特记忆。"
        elif 2001 <= 年份 <= 2005:
            return "新世纪初的中国，经济快速发展，互联网开始普及。\n手机、网吧、QQ和超女选秀风靡全国，SARS疫情给人们留下深刻印记。"
        elif 2006 <= 年份 <= 2010:
            return "中国迅速崛起的时期，北京奥运会展示国家形象，互联网全面普及。\n智能手机兴起，网络文化蓬勃发展，微博开始改变人们的生活方式。"
        else:
            return None
            
    def 显示事件(self, 事件名, 描述):
        """显示事件信息，带有动画效果
        
        参数:
            事件名(str): 事件名称
            描述(str): 事件描述
        """
        self.清屏()
        self.显示标题()
        
        # 创建事件面板背景
        面板背景 = pygame.Rect(20, 110, self.屏幕宽度 - 40, 460)
        pygame.draw.rect(self.主缓冲区, (35, 40, 50), 面板背景, border_radius=10)
        pygame.draw.rect(self.主缓冲区, (70, 100, 150), 面板背景, border_radius=10, width=2)
        
        # 记录脏矩形
        self.脏矩形列表.append(面板背景)
        
        # 绘制事件标题
        标题背景 = pygame.Rect(40, 130, self.屏幕宽度 - 80, 50)
        pygame.draw.rect(self.主缓冲区, (50, 60, 80), 标题背景, border_radius=8)
        
        # 记录脏矩形
        self.脏矩形列表.append(标题背景)
        
        self.绘制文本(f"【历史事件】: {事件名}", self.屏幕宽度//2, 155, self.高亮色, self.正文字体, True, True)
        
        # 处理长文本，按行分割并显示
        行高 = 30
        行数 = 0
        文本区域 = pygame.Rect(60, 200, self.屏幕宽度 - 120, 350)
        
        # 记录脏矩形
        self.脏矩形列表.append(文本区域)
        
        # 添加文本渐入效果
        for 段落 in 描述.split('\n'):
            字符数 = 0
            当前行 = ""
            
            for 字符 in 段落:
                当前行 += 字符
                字符数 += 1
                
                # 按宽度换行
                if 字符数 > 60:  # 每行约60个字符
                    # 使用渐变效果显示文本
                    动画延迟 = 行数 * 3
                    动画进度 = min(1.0, max(0, (self.帧计数 - 动画延迟) / 10))
                    
                    self.绘制文本(当前行, 60, 200 + 行数 * 行高)
                    行数 += 1
                    当前行 = ""
                    字符数 = 0
                    
            # 显示最后一行
            if 当前行:
                self.绘制文本(当前行, 60, 200 + 行数 * 行高)
                行数 += 1
                
            行数 += 0.5  # 段落之间增加间距
        
        # 将主缓冲区内容更新到屏幕
        self.屏幕.blit(self.主缓冲区, (0, 0))
        pygame.display.update(self.脏矩形列表)
        
    def 显示事件结果(self, 结果文本):
        """显示事件结果
        
        参数:
            结果文本(str): 事件结果描述
        """
        y = self.屏幕高度 - 150
        
        # 创建结果背景
        结果背景 = pygame.Rect(10, y - 10, self.屏幕宽度 - 20, 70)
        pygame.draw.rect(self.主缓冲区, (40, 45, 55), 结果背景, border_radius=8)
        pygame.draw.rect(self.主缓冲区, (70, 100, 150), 结果背景, border_radius=8, width=2)
        
        # 记录脏矩形
        self.脏矩形列表.append(结果背景)
        
        self.绘制文本("【结果】", 20, y, self.高亮色)
        self.绘制文本(结果文本, 20, y + 40)
        
        # 绘制继续按钮
        self.绘制按钮("继续", self.屏幕宽度//2 - 100, self.屏幕高度 - 80, 200, 40, self.显示主菜单)
        
        # 将主缓冲区内容更新到屏幕
        self.屏幕.blit(self.主缓冲区, (0, 0))
        pygame.display.update(self.脏矩形列表)
        
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
        
    def 显示主菜单(self, *args):
        """显示游戏主菜单
        
        参数:
            玩家信息(dict): 玩家基本信息字典
        """
        self.清屏()
        self.显示标题()
        self.按钮列表 = []  # 清空按钮列表
        
        # 重置消息
        self.消息 = ""
        self.消息计时器 = 0
        
        # 确保底部区域干净
        self.清除底部区域()
        
        # 更新当前界面状态
        self.当前界面 = "主菜单"
        
        选项 = ["探索当前时间", "查看个人属性", "查看收藏品", "时间推进", "保存游戏", "退出游戏"]
        
        if self.玩家信息:
            # 创建信息面板背景
            信息面板 = pygame.Rect(20, 100, self.屏幕宽度 - 40, 60)
            pygame.draw.rect(self.主缓冲区, (40, 45, 55), 信息面板, border_radius=10)
            pygame.draw.rect(self.主缓冲区, (70, 100, 150), 信息面板, border_radius=10, width=2)
            
            # 记录脏矩形
            self.脏矩形列表.append(信息面板)
            
            # 创建分隔线
            分隔线位置 = self.屏幕宽度 // 2
            pygame.draw.line(self.主缓冲区, (100, 120, 170), 
                          (分隔线位置, 105), (分隔线位置, 155), 1)
            
            # 显示玩家基本信息（左侧）
            self.绘制文本(f"玩家: {self.玩家信息['名字']}", 
                       self.屏幕宽度//4, 120, self.文本色, self.正文字体, True)
            self.绘制文本(f"年龄: {self.玩家信息['年龄']} 岁", 
                       self.屏幕宽度//4, 145, self.文本色, self.正文字体, True)
            
            # 显示游戏进度信息（右侧）
            self.绘制文本(f"当前年份: {self.玩家信息['当前年份']} 年", 
                       self.屏幕宽度//4 * 3, 120, self.文本色, self.正文字体, True)
            self.绘制文本(f"收藏品: {self.玩家信息['收藏品数量']} | 事件: {self.玩家信息['已触发事件数']}", 
                       self.屏幕宽度//4 * 3, 145, self.文本色, self.正文字体, True)
            
            # 绘制当前章节信息（居中，下方）
            章节背景 = pygame.Rect(self.屏幕宽度//2 - 100, 180, 200, 30)
            pygame.draw.rect(self.主缓冲区, (50, 60, 90), 章节背景, border_radius=5)
            self.脏矩形列表.append(章节背景)
            self.绘制文本(f"当前: {self.玩家信息['当前章节']}", 
                       self.屏幕宽度//2, 195, self.高亮色, self.正文字体, True)
            
            # 绘制主菜单图标和装饰
            self.绘制文本("主菜单", self.屏幕宽度//2, 230, self.高亮色, self.正文字体, True, True)
            
            # 绘制装饰线
            装饰线矩形 = pygame.Rect(self.屏幕宽度//2 - 100, 240, 200, 2)
            pygame.draw.line(self.主缓冲区, self.高亮色, (self.屏幕宽度//2 - 100, 240), 
                           (self.屏幕宽度//2 + 100, 240), 2)
            self.脏矩形列表.append(装饰线矩形)
            
            # 绘制选项按钮
            y = 270
            for i, 选项文本 in enumerate(选项):
                按钮 = self.绘制按钮(选项文本, self.屏幕宽度//2 - 150, y, 300, 50, None, i)
                y += 60
                
        else:
            # 如果没有玩家信息，显示游戏开始菜单
            选项 = ["开始新游戏", "加载游戏", "退出"]
            
            # 添加开场动画效果（仅在主菜单时）
            时间偏移 = math.sin(self.帧计数 * 0.03) * 5
            
            # 添加游戏介绍文本
            self.绘制文本("重返90后的童年岁月，体验那个年代的记忆", 
                       self.屏幕宽度//2, 150 + 时间偏移, self.高亮色, self.正文字体, True, True)
            
            # 绘制选项按钮
            y = 230
            for i, 选项文本 in enumerate(选项):
                按钮 = self.绘制按钮(选项文本, self.屏幕宽度//2 - 150, y, 300, 50, None, i)
                y += 100
            
            # 添加底部版权信息
            self.绘制文本("v1.0 © 2023 九零后时光机", 
                       self.屏幕宽度//2, self.屏幕高度 - 20, 
                       (150, 150, 150), self.小字体, True)
        
        # 将主缓冲区内容更新到屏幕
        self.屏幕.blit(self.主缓冲区, (0, 0))
        pygame.display.update(self.脏矩形列表)
        
    def 输入选择(self, 选项列表, 提示="请选择:"):
        """使用图形界面提供选项列表，获取用户选择
        
        参数:
            选项列表(list): 选项文本列表
            提示(str): 提示文本
            
        返回:
            int: 用户选择的选项索引（从0开始）
        """
        self.选项列表 = 选项列表
        self.按钮列表 = []
        
        self.清屏()
        self.显示标题()
        
        # 绘制选择面板背景
        选择面板 = pygame.Rect(20, 110, self.屏幕宽度 - 40, 450)
        pygame.draw.rect(self.主缓冲区, (35, 40, 50), 选择面板, border_radius=10)
        pygame.draw.rect(self.主缓冲区, (70, 100, 150), 选择面板, border_radius=10, width=2)
        
        # 记录脏矩形
        self.脏矩形列表.append(选择面板)
        
        # 绘制提示文本
        self.绘制文本(提示, 20, 120, self.高亮色)
        
        # 绘制装饰线
        装饰线矩形 = pygame.Rect(20, 150, self.屏幕宽度 - 40, 2)
        pygame.draw.line(self.主缓冲区, (70, 100, 150), (20, 150), (self.屏幕宽度 - 20, 150), 2)
        self.脏矩形列表.append(装饰线矩形)
        
        y = 180
        for i, 选项文本 in enumerate(选项列表):
            按钮 = self.绘制按钮(选项文本, self.屏幕宽度//2 - 150, y, 300, 50, None, i)
            y += 70
            
        # 将主缓冲区内容更新到屏幕
        self.屏幕.blit(self.主缓冲区, (0, 0))
        pygame.display.update(self.脏矩形列表)
        
        # 等待用户选择
        选择结果 = None
        等待中 = True
        
        while 等待中:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # 左键点击
                    for i, 按钮 in enumerate(self.按钮列表):
                        if 按钮["矩形"].collidepoint(event.pos):
                            选择结果 = 按钮["参数"]
                            等待中 = False
            
            self.时钟.tick(30)  # 限制帧率
            
        return 选择结果
        
    def 获取输入(self, 提示):
        """获取用户输入文本，带有动画和视觉效果
        
        参数:
            提示(str): 输入提示文本
            
        返回:
            str: 用户输入的文本
        """
        self.清屏()
        self.显示标题()
        
        # 初始化pygame输入法
        pygame.key.start_text_input()
        
        # 创建输入面板背景
        面板背景 = pygame.Rect(50, 100, self.屏幕宽度 - 100, 200)
        pygame.draw.rect(self.主缓冲区, (35, 40, 50), 面板背景, border_radius=15)
        pygame.draw.rect(self.主缓冲区, (70, 100, 150), 面板背景, border_radius=15, width=2)
        
        # 记录脏矩形
        self.脏矩形列表.append(面板背景)
        
        # 绘制提示文本
        self.绘制文本(提示, self.屏幕宽度//2, 140, self.高亮色, self.正文字体, True, True)
        
        # 绘制输入框
        输入框 = pygame.Rect(100, 180, self.屏幕宽度 - 200, 50)
        pygame.draw.rect(self.主缓冲区, (50, 50, 50), 输入框, border_radius=8)
        pygame.draw.rect(self.主缓冲区, (100, 150, 200), 输入框, border_radius=8, width=2)
        
        # 记录脏矩形
        self.脏矩形列表.append(输入框)
        
        # 将主缓冲区内容更新到屏幕
        self.屏幕.blit(self.主缓冲区, (0, 0))
        pygame.display.update(self.脏矩形列表)
        
        当前输入 = ""
        输入活动 = True
        确认按钮 = None
        
        while 输入活动:
            # 更新背景动画
            self.帧计数 += 1
            self.清屏()
            self.显示标题()
            
            # 重新绘制输入面板
            pygame.draw.rect(self.主缓冲区, (35, 40, 50), 面板背景, border_radius=15)
            pygame.draw.rect(self.主缓冲区, (70, 100, 150), 面板背景, border_radius=15, width=2)
            self.绘制文本(提示, self.屏幕宽度//2, 140, self.高亮色, self.正文字体, True, True)
            
            # 重新绘制输入框和文本
            pygame.draw.rect(self.主缓冲区, (50, 50, 50), 输入框, border_radius=8)
            pygame.draw.rect(self.主缓冲区, (100, 150, 200), 输入框, border_radius=8, width=2)
            
            输入文本 = self.正文字体.render(当前输入, True, self.文本色)
            self.主缓冲区.blit(输入文本, (输入框.x + 15, 输入框.y + 15))
            
            # 绘制闪烁的光标
            if pygame.time.get_ticks() % 1000 < 500:
                光标位置 = self.正文字体.size(当前输入)[0] + 输入框.x + 15
                光标矩形 = pygame.Rect(光标位置, 输入框.y + 12, 2, 26)
                pygame.draw.line(self.主缓冲区, self.文本色, 
                              (光标位置, 输入框.y + 12), 
                              (光标位置, 输入框.y + 38), 2)
                self.脏矩形列表.append(光标矩形)
            
            # 绘制确认按钮（只要有输入就显示）
            if 当前输入:
                self.按钮列表 = []
                确认按钮 = self.绘制按钮("确认", self.屏幕宽度//2 - 50, 260, 100, 40, None, None)
            
            # 将主缓冲区内容更新到屏幕
            self.屏幕.blit(self.主缓冲区, (0, 0))
            pygame.display.update(self.脏矩形列表)
            
            # 处理输入事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if 当前输入:  # 有内容时才允许确认
                            输入活动 = False
                    elif event.key == pygame.K_BACKSPACE:
                        当前输入 = 当前输入[:-1]
                    else:
                        当前输入 += event.unicode
                elif event.type == pygame.TEXTINPUT:
                    # 处理文本输入事件 (支持中文输入)
                    当前输入 += event.text
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # 左键点击确认按钮
                    if 确认按钮 and 当前输入:
                        # 检查是否点击了确认按钮
                        for 按钮 in self.按钮列表:
                            if 按钮["矩形"].collidepoint(event.pos):
                                输入活动 = False
                                break
            
            self.时钟.tick(30)
            
        # 结束文本输入
        pygame.key.stop_text_input()
        
        # 输入完成后，显示处理中动画
        if 当前输入:
            # 清除输入界面
            self.清屏()
            self.显示标题()
            
            # 绘制确认信息
            确认背景 = pygame.Rect(50, 200, self.屏幕宽度 - 100, 100)
            pygame.draw.rect(self.主缓冲区, (35, 40, 50), 确认背景, border_radius=15)
            pygame.draw.rect(self.主缓冲区, (70, 100, 150), 确认背景, border_radius=15, width=2)
            
            self.绘制文本(f"你好, {当前输入}! 正在准备游戏...", self.屏幕宽度//2, 220, self.高亮色, self.正文字体, True, True)
            
            # 绘制加载动画
            加载动画起点 = self.屏幕宽度//2 - 50
            pygame.draw.rect(self.主缓冲区, (60, 120, 190), pygame.Rect(加载动画起点, 260, 100, 10), border_radius=5)
            
            # 更新屏幕
            self.屏幕.blit(self.主缓冲区, (0, 0))
            pygame.display.flip()
            
            # 短暂延迟，让用户看到确认信息
            pygame.time.wait(800)
            
            # 再次清屏，准备显示游戏主界面
            self.清屏()
        
        return 当前输入
        
    def 显示加载成功(self, 玩家名字, 年份):
        """显示游戏加载成功信息
        
        参数:
            玩家名字(str): 玩家名字
            年份(int): 当前游戏年份
        """
        self.显示文本(f"欢迎回来，{玩家名字}！现在是{年份}年", 2)
        
    def 显示保存成功(self, 玩家名字, 年份):
        """显示游戏保存成功信息
        
        参数:
            玩家名字(str): 玩家名字
            年份(int): 当前游戏年份
        """
        self.显示文本(f"游戏已保存 - {玩家名字}的{年份}年生活", 2)
        
    def 显示时间推进(self, 年份, 章节):
        """显示时间推进信息
        
        参数:
            年份(int): 新的年份
            章节(str): 新的章节
        """
        self.清屏()
        self.显示标题()
        
        # 创建时间推进面板背景
        面板背景 = pygame.Rect(50, 170, self.屏幕宽度 - 100, 250)
        pygame.draw.rect(self.主缓冲区, (35, 40, 50), 面板背景, border_radius=15)
        pygame.draw.rect(self.主缓冲区, (70, 100, 150), 面板背景, border_radius=15, width=2)
        
        # 记录脏矩形
        self.脏矩形列表.append(面板背景)
        
        # 绘制文本
        self.绘制文本("时光机启动...", self.屏幕宽度//2, 200, self.高亮色, self.标题字体, True)
        
        # 更新屏幕
        self.屏幕.blit(self.主缓冲区, (0, 0))
        pygame.display.update(self.脏矩形列表)
        pygame.time.wait(1000)
        
        # 清空脏矩形列表，为新的渲染做准备
        self.脏矩形列表 = []
        
        # 绘制年份文本
        self.绘制文本(f"年份推进到: {年份}年", self.屏幕宽度//2, 250, self.文本色, self.标题字体, True)
        
        # 更新屏幕
        self.屏幕.blit(self.主缓冲区, (0, 0))
        pygame.display.update(self.脏矩形列表)
        pygame.time.wait(800)
        
        # 清空脏矩形列表，为新的渲染做准备
        self.脏矩形列表 = []
        
        # 绘制章节文本
        self.绘制文本(f"当前章节: {章节}", self.屏幕宽度//2, 300, self.文本色, self.标题字体, True)
        
        # 更新屏幕
        self.屏幕.blit(self.主缓冲区, (0, 0))
        pygame.display.update(self.脏矩形列表)
        pygame.time.wait(1000)
        
        # 绘制继续按钮
        self.绘制按钮("继续", self.屏幕宽度//2 - 100, self.屏幕高度 - 80, 200, 40, self.显示主菜单)
        
        # 最后一次更新屏幕
        self.屏幕.blit(self.主缓冲区, (0, 0))
        pygame.display.update(self.脏矩形列表)
        
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
            
    def 播放音效(self, 音效名):
        """播放指定音效
        
        参数:
            音效名(str): 音效名称
        """
        # 实现音效播放功能
        pass
        
    def 设置玩家信息(self, 玩家信息):
        """设置玩家信息
        
        参数:
            玩家信息(dict): 玩家信息字典
        """
        self.玩家信息 = 玩家信息
        
    def 设置回调(self, 回调函数):
        """设置回调函数
        
        参数:
            回调函数: 回调函数
        """
        self.回调 = 回调函数
        
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
                        if 按钮["操作"]:
                            # 如果按钮有操作函数，调用它
                            if 按钮["参数"] is not None:
                                按钮["操作"](按钮["参数"])
                            else:
                                按钮["操作"]()
                        elif self.回调:
                            # 否则调用全局回调
                            self.回调(按钮["参数"])
                        break
                        
    def 更新(self):
        """更新界面状态"""
        # 增加帧计数器
        self.帧计数 += 1
        
        # 清空脏矩形列表
        self.脏矩形列表 = []
        
        # 重新绘制按钮，处理鼠标悬停效果
        self.按钮列表 = []
        
        if self.当前界面 == "主菜单":
            self.显示主菜单()
            
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
        
        self.处理事件()
        
        # 从主缓冲区更新到屏幕，只更新脏矩形区域
        if self.脏矩形列表:
            # 将主缓冲区内容绘制到屏幕
            self.屏幕.blit(self.主缓冲区, (0, 0))
            # 仅更新脏矩形区域，而不是整个屏幕
            pygame.display.update(self.脏矩形列表)
        else:
            # 如果没有脏矩形，则更新整个屏幕（首次渲染或全屏更新）
            self.屏幕.blit(self.主缓冲区, (0, 0))
            pygame.display.flip()
        
    def 运行(self):
        """运行游戏主循环"""
        self.运行中 = True
        
        # 重置消息
        self.消息 = ""
        self.消息计时器 = 0
        
        # 首次清屏，确保背景正确绘制
        self.清屏()
        self.清除底部区域()
        self.屏幕.blit(self.主缓冲区, (0, 0))
        pygame.display.flip()
        
        while self.运行中:
            self.更新()
            self.时钟.tick(30)  # 限制帧率为30FPS

def 创建图形界面():
    """创建图形界面实例
    
    返回:
        图形界面: 界面实例
    """
    return 图形界面() 