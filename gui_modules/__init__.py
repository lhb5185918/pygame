#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gui_modules.gui_base import GUI基础类
from gui_modules.gui_manager import GUI管理器
from gui_modules.gui_main_menu import 主菜单界面
from gui_modules.gui_collection import 收藏品界面
from gui_modules.gui_attributes import 属性界面
from gui_modules.gui_events import 事件界面
from gui_modules.gui_time import 时间界面
from gui_modules.gui_input import 输入界面

# 创建GUI界面的工厂函数
def 创建图形界面():
    """创建图形界面实例
    
    返回:
        GUI管理器: 界面管理器实例
    """
    return GUI管理器() 