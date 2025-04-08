#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config

class 玩家角色:
    """玩家角色类，管理玩家的属性、收藏品和历史选择"""
    
    def __init__(self, 名字=""):
        """初始化玩家角色"""
        self.名字 = 名字
        self.当前年份 = config.STARTING_YEAR
        self.属性 = config.DEFAULT_ATTRIBUTES.copy()
        self.收藏品 = []
        self.已触发事件 = []
        self.历史选择 = {}
        self._更新章节()
    
    def _更新章节(self):
        """根据当前年份更新学习/工作章节"""
        年龄 = self.当前年份 - config.BIRTH_YEAR
        
        if 年龄 in config.AGE_TO_GRADE:
            阶段, 年级 = config.AGE_TO_GRADE[年龄]
            self.当前章节 = f"{阶段}{年级}年级"
        else:
            self.当前章节 = "工作阶段"
    
    def 时间推进(self):
        """推进游戏时间到下一年"""
        if self.当前年份 < config.ENDING_YEAR:
            self.当前年份 += 1
            self._更新章节()
            return True
        return False
    
    def 属性变化(self, 属性名, 变化值):
        """修改玩家属性值
        
        参数:
            属性名(str): 要修改的属性名称
            变化值(int): 属性的变化值，可为正或负
            
        返回:
            tuple: (变化描述, 新属性值)
        """
        if 属性名 in self.属性:
            原值 = self.属性[属性名]
            self.属性[属性名] += 变化值
            # 确保属性值在0-100之间
            self.属性[属性名] = max(0, min(100, self.属性[属性名]))
            变化描述 = "增加" if 变化值 > 0 else "减少"
            return (变化描述, abs(变化值), self.属性[属性名])
        return None
    
    def 添加收藏品(self, 收藏品名):
        """添加收藏品到玩家收藏列表
        
        参数:
            收藏品名(str): 收藏品名称
            
        返回:
            bool: 是否成功添加（如果已存在则返回False）
        """
        if 收藏品名 not in self.收藏品:
            self.收藏品.append(收藏品名)
            return True
        return False
    
    def 记录事件选择(self, 事件名, 选择):
        """记录玩家在特定事件中做出的选择
        
        参数:
            事件名(str): 事件名称
            选择(int/str): 玩家的选择
        """
        self.历史选择[事件名] = 选择
        
    def 记录已触发事件(self, 事件名):
        """记录已经触发过的事件，避免重复触发
        
        参数:
            事件名(str): 事件名称
        """
        if 事件名 not in self.已触发事件:
            self.已触发事件.append(事件名)
    
    def 获取属性进度条(self, 属性名):
        """获取属性的进度条可视化
        
        参数:
            属性名(str): 属性名称
            
        返回:
            str: 进度条字符串
        """
        if 属性名 in self.属性:
            值 = self.属性[属性名]
            进度条 = "█" * (值 // 10) + "░" * (10 - 值 // 10)
            return f"{属性名}: {进度条} {值}/100"
        return ""
    
    def 获取所有属性(self):
        """获取玩家所有属性和值
        
        返回:
            dict: 属性名和值的字典
        """
        return self.属性.copy()
    
    def 获取基本信息(self):
        """获取玩家的基本信息
        
        返回:
            dict: 包含玩家基本信息的字典
        """
        年龄 = self.当前年份 - config.BIRTH_YEAR
        return {
            "名字": self.名字,
            "当前年份": self.当前年份,
            "当前章节": self.当前章节,
            "年龄": 年龄,
            "收藏品数量": len(self.收藏品),
            "已触发事件数": len(self.已触发事件)
        }
        
    def 获取收藏品列表(self):
        """获取玩家收藏品列表
        
        返回:
            list: 收藏品列表
        """
        return self.收藏品.copy()
    
    def 获取未触发事件(self, 年份事件列表):
        """获取给定年份中未触发过的事件
        
        参数:
            年份事件列表(list): 特定年份的所有事件
            
        返回:
            list: 未触发过的事件列表
        """
        return [事件 for 事件 in 年份事件列表 if 事件 not in self.已触发事件] 