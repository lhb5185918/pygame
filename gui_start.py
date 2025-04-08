#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
九零后时光机 - 图形界面启动器
启动图形界面版本的游戏
"""

from game_engine import 游戏引擎

if __name__ == "__main__":
    print("正在启动九零后时光机图形界面版...")
    引擎 = 游戏引擎(使用图形界面=True)
    引擎.启动游戏() 