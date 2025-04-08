#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import os

try:
    import curses

    CURSES_AVAILABLE = True
except ImportError:
    CURSES_AVAILABLE = False
    print("警告：未找到curses库，将使用简易文本界面")

try:
    import pygame

    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("警告：未找到pygame库，音效功能不可用")


class 简易界面:
    """简易文本界面类，处理基本的文本显示和输入"""

    def __init__(self, 标题="九零后时光机"):
        """初始化简易界面
        
        参数:
            标题(str): 游戏标题
        """
        self.标题 = 标题
        self.清屏()

    def 清屏(self):
        """清除终端屏幕内容"""
        # 根据操作系统选择清屏命令
        os.system('cls' if os.name == 'nt' else 'clear')

    def 显示文本(self, 文本, 延迟=0):
        """显示文本，可设置延迟
        
        参数:
            文本(str): 要显示的文本
            延迟(float): 显示后的延迟时间（秒）
        """
        print(文本)
        if 延迟 > 0:
            time.sleep(延迟)

    def 显示标题(self):
        """显示游戏标题"""
        self.清屏()
        标题线 = "=" * (len(self.标题) + 10)
        print(f"\n{标题线}")
        print(f"    {self.标题}    ")
        print(f"{标题线}\n")

    def 显示ASCII艺术(self, 文本):
        """显示ASCII艺术文本
        
        参数:
            文本(str): ASCII艺术文本
        """
        print(文本)

    def 输入选择(self, 选项列表, 提示="请选择:"):
        """提供选项列表，获取用户选择
        
        参数:
            选项列表(list): 选项文本列表
            提示(str): 提示文本
            
        返回:
            int: 用户选择的选项索引（从0开始）
        """
        print(f"\n{提示}")
        for i, 选项 in enumerate(选项列表, 1):
            print(f"{i}. {选项}")

        while True:
            try:
                选择 = input("输入选项编号: ")
                选择 = int(选择)
                if 1 <= 选择 <= len(选项列表):
                    return 选择 - 1  # 转换为从0开始的索引
                else:
                    print("无效选择，请重试")
            except ValueError:
                print("请输入数字")

    def 获取输入(self, 提示):
        """获取用户输入文本
        
        参数:
            提示(str): 输入提示文本
            
        返回:
            str: 用户输入的文本
        """
        return input(f"{提示}: ")

    def 显示属性(self, 属性字典):
        """显示玩家属性值
        
        参数:
            属性字典(dict): 属性名和值的字典
        """
        print("\n【个人属性】")
        for 属性, 值 in 属性字典.items():
            进度条 = "█" * (值 // 10) + "░" * (10 - 值 // 10)
            print(f"{属性}: {进度条} {值}/100")

    def 显示收藏品(self, 收藏品列表):
        """显示玩家的收藏品
        
        参数:
            收藏品列表(list): 收藏品名称列表
        """
        if not 收藏品列表:
            print("\n你还没有收集到任何宝贵的童年收藏品。")
            return

        print("\n【童年收藏品】")
        for i, 收藏品 in enumerate(收藏品列表, 1):
            print(f"{i}. {收藏品}")

    def 显示属性变化(self, 属性名, 描述, 变化值, 当前值):
        """显示属性变化信息
        
        参数:
            属性名(str): 属性名称
            描述(str): 变化描述（"增加"或"减少"）
            变化值(int): 变化的数值
            当前值(int): 变化后的当前值
        """
        print(f"{属性名}{描述}了{变化值}点 (当前值: {当前值})")

    def 显示事件(self, 事件名, 描述):
        """显示事件信息
        
        参数:
            事件名(str): 事件名称
            描述(str): 事件描述
        """
        print(f"\n【历史事件】: {事件名}")
        print(描述)

    def 显示事件结果(self, 结果文本):
        """显示事件结果
        
        参数:
            结果文本(str): 事件结果描述
        """
        print(f"\n【结果】: {结果文本}")

    def 显示主菜单(self, 玩家信息):
        """显示游戏主菜单
        
        参数:
            玩家信息(dict): 玩家基本信息字典
        """
        self.显示标题()
        print(f"玩家: {玩家信息['名字']} | 年份: {玩家信息['当前年份']} | 阶段: {玩家信息['当前章节']}")
        print(f"年龄: {玩家信息['年龄']} | 收藏品: {玩家信息['收藏品数量']} | 经历事件: {玩家信息['已触发事件数']}")
        print("\n【主菜单】")
        选项 = ["探索当前时间", "查看个人属性", "查看收藏品", "时间推进", "保存游戏", "退出游戏"]
        return self.输入选择(选项, "请选择操作")

    def 显示年代特色(self, 年份, 特色列表):
        """显示特定年份的文化特色
        
        参数:
            年份(int): 年份
            特色列表(list): 特色描述列表
        """
        print(f"\n【{年份}年的流行元素】")
        for 特色 in 特色列表:
            print(f"· {特色}")

    def 显示加载成功(self, 玩家名字, 年份):
        """显示游戏加载成功信息
        
        参数:
            玩家名字(str): 玩家名字
            年份(int): 当前游戏年份
        """
        print(f"欢迎回来，{玩家名字}！现在是{年份}年")

    def 显示保存成功(self, 玩家名字, 年份):
        """显示游戏保存成功信息
        
        参数:
            玩家名字(str): 玩家名字
            年份(int): 当前游戏年份
        """
        print(f"游戏已保存 - {玩家名字}的{年份}年生活")

    def 显示时间推进(self, 年份, 章节):
        """显示时间推进信息
        
        参数:
            年份(int): 新的年份
            章节(str): 新的章节
        """
        print(f"\n时光机启动...\n年份推进到: {年份}年")
        print(f"当前章节: {章节}")

    def 等待按键(self, 提示="按回车键继续..."):
        """等待用户按键继续
        
        参数:
            提示(str): 提示文本
        """
        input(提示)

    def 播放音效(self, 音效名):
        """播放指定音效（如果pygame可用）
        
        参数:
            音效名(str): 音效名称
        """
        # 如果pygame可用，此处可以实现音效播放
        pass


class 高级界面(简易界面):
    """使用curses库的高级文本界面类，支持更丰富的显示效果"""

    def __init__(self, 标题="九零后时光机"):
        """初始化高级界面
        
        参数:
            标题(str): 游戏标题
        """
        if not CURSES_AVAILABLE:
            super().__init__(标题)
            return

        self.标题 = 标题
        self.stdscr = None
        # 高级界面初始化在start方法中完成

    def start(self):
        """启动curses界面模式"""
        if not CURSES_AVAILABLE:
            return

        self.stdscr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)  # 绿色文本
        curses.init_pair(2, curses.COLOR_YELLOW, -1)  # 黄色文本
        curses.init_pair(3, curses.COLOR_CYAN, -1)  # 青色文本
        curses.init_pair(4, curses.COLOR_RED, -1)  # 红色文本
        curses.cbreak()
        curses.noecho()
        self.stdscr.keypad(True)
        self.stdscr.clear()

    def stop(self):
        """停止curses界面模式"""
        if not CURSES_AVAILABLE or self.stdscr is None:
            return

        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    # 重写部分方法以适应curses界面
    # 具体实现可根据需要添加


def 创建界面(使用高级界面=False):
    """创建并返回适当的界面实例
    
    参数:
        使用高级界面(bool): 是否使用高级界面
        
    返回:
        Interface: 界面实例
    """
    if 使用高级界面 and CURSES_AVAILABLE:
        return 高级界面()
    else:
        return 简易界面()
