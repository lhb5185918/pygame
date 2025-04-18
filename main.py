#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
九零后时光机 - 一个文字冒险游戏
重返90后的童年岁月，体验那些年的记忆
"""

import os
import sys
import argparse
import pygame
from game_engine import 游戏引擎
from gui import GUI

def main():
    """程序主入口点"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="九零后时光机 - 重返那些年的日子")
    parser.add_argument('--高级界面', action='store_true', default=False, 
                        help='使用高级终端界面(需要curses库)')
    parser.add_argument('--无声音', action='store_true', default=False,
                        help='禁用游戏音效')
    parser.add_argument('--图形界面', action='store_true', default=False,
                        help='使用图形界面模式(需要pygame库)')
    args = parser.parse_args()
    
    try:
        # 创建游戏引擎
        引擎 = 游戏引擎(使用高级界面=args.高级界面, 使用图形界面=args.图形界面)
        
        # 初始化GUI
        gui = GUI(宽度=800, 高度=600)
        
        # 启动游戏
        引擎.启动游戏()
        
        # 运行GUI主循环
        gui.运行()
    except KeyboardInterrupt:
        print("\n游戏被中断")
    except Exception as e:
        print(f"游戏出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 确保程序正常退出
        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    main() 