#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import sys
from gui import GUI

def main():
    """程序主入口点"""
    # 初始化GUI
    gui = GUI(宽度=800, 高度=600)
    
    try:
        # 运行GUI主循环
        gui.运行()
    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1)
    finally:
        # 确保程序正常退出
        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    main() 