#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import datetime
import config
from player import 玩家角色
from save_system import 存档系统
import events_data
import ui
from holidays_system import 节日系统
import holiday_events
from random_events import RandomEventSystem
import math
import sys

try:
    from gui import 创建图形界面
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    print("警告：图形界面初始化失败，将使用文本界面")

class 游戏引擎:
    """游戏引擎，协调各个模块工作"""
    
    def __init__(self, 使用高级界面=False, 使用图形界面=False):
        """初始化游戏引擎
        
        参数:
            使用高级界面(bool): 是否使用高级界面
            使用图形界面(bool): 是否使用图形界面
        """
        # 选择界面类型
        self.使用图形界面 = 使用图形界面 and GUI_AVAILABLE
        
        if self.使用图形界面:
            self.界面 = 创建图形界面()
            self.界面.设置回调(self.处理界面回调)
        else:
            self.界面 = ui.创建界面(使用高级界面)
            
        self.存档系统 = 存档系统()
        self.节日系统 = 节日系统()
        self.玩家 = None
        self.运行中 = False
        self.当前日期 = None
        
        # 初始化随机事件系统
        self.random_event_system = RandomEventSystem()
    
    def 开始新游戏(self):
        """开始新游戏"""
        if self.使用图形界面:
            玩家名字 = self.界面.获取输入("请输入你的名字")
            
            if not 玩家名字:
                玩家名字 = "小明"  # 默认名字
                
            # 创建新玩家
            self.玩家 = 玩家角色(玩家名字)
            
            # 更新图形界面中的玩家信息
            self.界面.设置玩家信息(self.获取玩家信息())
            self.界面.显示文本(f"你好，{玩家名字}！欢迎回到{self.玩家.当前年份}年...", 1)
            
            # 初始化游戏日期
            self.当前日期 = datetime.date(self.玩家.当前年份, 1, 1)
            self.运行中 = True
            
            # 显示主菜单，确保界面切换，不留下输入姓名的界面
            self.界面.显示主菜单()
            
            # 图形界面模式不需要进入主循环，会通过回调处理
            return
        
        # 原有的文本界面逻辑
        self.界面.显示ASCII艺术(config.WELCOME_ASCII)
        玩家名字 = self.界面.获取输入("请输入你的名字")
        
        if not 玩家名字:
            玩家名字 = "小明"  # 默认名字
            
        # 选择地区（影响春节习俗）
        地区选项 = ["北方", "南方"]
        地区选择 = self.界面.输入选择(地区选项, "请选择你的家乡区域:")
        选定地区 = 地区选项[地区选择]
        self.节日系统.设置区域(选定地区)
            
        self.玩家 = 玩家角色(玩家名字)
        self.界面.显示文本(f"你好，{玩家名字}！欢迎回到{self.玩家.当前年份}年...", 1)
        self.界面.显示文本(f"那时的你，正坐在{self.玩家.当前章节}的教室里...", 1)
        
        # 初始化游戏日期（默认为该年1月1日）
        self.当前日期 = datetime.date(self.玩家.当前年份, 1, 1)
        
        self.运行中 = True
        self.主循环()
    
    def 加载游戏(self):
        """加载游戏存档"""
        存档列表 = self.存档系统.列出存档()
        
        if not 存档列表:
            self.界面.显示文本("没有找到游戏存档。")
            self.界面.等待按键()
            return False
        
        选项 = [f"{文件名} - {时间} ({大小}KB)" for 文件名, 时间, 大小 in 存档列表]
        选项.append("返回")
        
        选择 = self.界面.输入选择(选项, "选择要加载的存档:")
        
        if 选择 == len(选项) - 1:  # 选择了"返回"
            return False
            
        存档名 = 存档列表[选择][0]
        self.玩家 = self.存档系统.加载游戏(存档名)
        
        if self.玩家:
            self.界面.显示加载成功(self.玩家.名字, self.玩家.当前年份)
            
            # 恢复游戏日期（默认为该年1月1日）
            if hasattr(self.玩家, '当前日期'):
                self.当前日期 = self.玩家.当前日期
            else:
                self.当前日期 = datetime.date(self.玩家.当前年份, 1, 1)
                
            self.运行中 = True
            self.主循环()
            return True
        else:
            self.界面.显示文本("加载存档失败。")
            self.界面.等待按键()
            return False
    
    def 保存游戏(self):
        """保存当前游戏"""
        if not self.玩家:
            return False
        
        # 保存当前日期到玩家对象    
        self.玩家.当前日期 = self.当前日期
            
        存档路径 = self.存档系统.保存游戏(self.玩家)
        self.界面.显示保存成功(self.玩家.名字, self.玩家.当前年份)
        self.界面.等待按键()
        return True
    
    def 主循环(self):
        """游戏主循环"""
        while self.运行中:
            # 检查当前是否是节日
            是否节日, 节日名 = self.节日系统.是否节日(
                self.当前日期.year, 
                self.当前日期.month, 
                self.当前日期.day
            )
            
            # 显示当前日期和节日信息
            日期信息 = f"{self.当前日期.year}年{self.当前日期.month}月{self.当前日期.day}日"
            if 是否节日:
                日期信息 += f" 【{节日名}】"
            
            # 首先检查是否有节日事件需要触发
            if 是否节日 and not self.节日系统.是否已触发节日(self.当前日期.year, 节日名):
                self.触发节日事件(节日名)
                # 标记该节日已触发
                self.节日系统.标记节日已触发(self.当前日期.year, 节日名)
            
            # 检查随机事件
            self.检查随机事件()
            
            # 正常菜单选择
            选择 = self.界面.显示主菜单(self.玩家.获取基本信息(), 日期信息)
            
            if 选择 == 0:  # 探索当前时间
                self.探索当前时间()
            elif 选择 == 1:  # 查看个人属性
                self.界面.显示属性(self.玩家.获取所有属性())
                self.界面.等待按键()
            elif 选择 == 2:  # 查看收藏品
                self.界面.显示收藏品(self.玩家.获取收藏品列表())
                self.界面.等待按键()
            elif 选择 == 3:  # 时间推进
                self.时间推进()
            elif 选择 == 4:  # 查看节日物品和记录
                self.显示节日收藏()
            elif 选择 == 5:  # 保存游戏
                self.保存游戏()
            elif 选择 == 6:  # 退出游戏
                self.运行中 = False
                self.界面.显示文本("感谢游玩《九零后时光机》！", 1)
    
    def 探索当前时间(self):
        """探索当前年份的特色和事件"""
        当前年份 = self.玩家.当前年份
        年份特色 = events_data.获取年份特色(当前年份)
        
        if not 年份特色:
            self.界面.显示文本("这一年的记忆还不太清晰...")
            self.界面.等待按键()
            return
            
        self.界面.显示年代特色(当前年份, 年份特色)
        
        探索选项 = ["去文具店", "在家看电视", "去同学家玩", "返回"]
        选择 = self.界面.输入选择(探索选项, "你想做什么:")
        
        if 选择 == 3:  # 选择了"返回"
            return
            
        # 根据选择触发随机事件
        可用事件 = self.玩家.获取未触发事件(events_data.获取年份事件(当前年份))
        
        if 可用事件:
            # 一定概率触发事件
            if random.random() < 0.7:  # 70%概率触发
                事件名 = random.choice(可用事件)
                self.触发事件(事件名)
            else:
                self.界面.显示文本("你度过了平静的一天，没有特别的事情发生。")
                self.界面.等待按键()
        else:
            self.界面.显示文本("这一年的大事件你都已经经历过了。")
            self.界面.等待按键()
    
    def 触发事件(self, 事件名):
        """触发特定事件
        
        参数:
            事件名(str): 要触发的事件名称
        """
        事件详情 = events_data.获取事件详情(事件名)
        
        if not 事件详情:
            self.界面.显示文本(f"事件 '{事件名}' 数据未定义。")
            self.界面.等待按键()
            return
            
        self.界面.显示事件(事件名, 事件详情["描述"])
        
        选项 = [选项["描述"] for 选项 in 事件详情["选项"]]
        选择索引 = self.界面.输入选择(选项, "你的选择是:")
        
        # 记录事件已触发
        self.玩家.记录已触发事件(事件名)
        self.玩家.记录事件选择(事件名, 选择索引)
        
        # 应用结果
        选择结果 = 事件详情["选项"][选择索引]
        self.界面.显示事件结果(选择结果["结果"])
        
        # 属性变化
        for 属性名, 变化值 in 选择结果.get("属性变化", {}).items():
            变化信息 = self.玩家.属性变化(属性名, 变化值)
            if 变化信息:
                描述, 数值, 当前值 = 变化信息
                self.界面.显示属性变化(属性名, 描述, 数值, 当前值)
        
        # 收藏品获取
        for 收藏品 in 选择结果.get("收藏品", []):
            if self.玩家.添加收藏品(收藏品):
                self.界面.显示文本(f"获得收藏品: {收藏品}")
        
        self.界面.等待按键()
    
    def 触发节日事件(self, 节日名):
        """触发特定节日的事件
        
        参数:
            节日名(str): 节日名称
        """
        # 获取随机节日事件
        事件名, 事件详情 = holiday_events.获取随机节日事件(节日名)
        
        if not 事件名 or not 事件详情:
            self.界面.显示文本(f"今天是{节日名}，但没有特别的事件发生。")
            self.界面.等待按键()
            return
            
        self.界面.显示节日(节日名, f"【{事件名}】\n{事件详情['描述']}")
        
        选项 = [选项["描述"] for 选项 in 事件详情["选项"]]
        选择索引 = self.界面.输入选择(选项, "你的选择是:")
        
        # 应用结果
        选择结果 = 事件详情["选项"][选择索引]
        self.界面.显示事件结果(选择结果["结果"])
        
        # 属性变化
        for 属性名, 变化值 in 选择结果.get("属性变化", {}).items():
            变化信息 = self.玩家.属性变化(属性名, 变化值)
            if 变化信息:
                描述, 数值, 当前值 = 变化信息
                self.界面.显示属性变化(属性名, 描述, 数值, 当前值)
        
        # 收藏品获取
        for 收藏品 in 选择结果.get("收藏品", []):
            if self.玩家.添加收藏品(收藏品):
                self.界面.显示文本(f"获得收藏品: {收藏品}")
                # 也添加到节日物品中
                self.节日系统.添加节日物品(收藏品)
        
        # 特殊处理：春节压岁钱
        if 节日名 == "春节" and "压岁钱加成" in 选择结果:
            压岁钱加成 = 选择结果["压岁钱加成"]
            压岁钱 = int(self.节日系统.计算压岁钱(self.当前日期.year) * 压岁钱加成)
            if 压岁钱 > 0:
                self.界面.显示文本(f"你收到了 {压岁钱} 元压岁钱！")
                self.节日系统.记录压岁钱(self.当前日期.year, 压岁钱)
                # 增加零花钱属性
                self.玩家.属性变化("零花钱", int(压岁钱 * 0.1))  # 只有10%直接计入零花钱
        
        # 特殊处理：拜年记录
        if 节日名 == "春节" and 事件名 == "拜年走亲戚" and 选择索引 != 2:  # 不是选"找借口不去"
            对象列表 = ["爷爷奶奶", "姥姥姥爷", "大伯一家", "二姨一家", "舅舅一家"]
            拜年对象 = random.sample(对象列表, min(3, len(对象列表)))
            for 对象 in 拜年对象:
                self.节日系统.记录拜年(self.当前日期.year, 对象)
                self.界面.显示文本(f"你拜访了{对象}")
        
        # 如果是贴春联等收集类活动
        if 节日名 == "春节" and 事件名 == "贴春联" and 选择索引 != 2:  # 不是选"观看但不参与"
            春联文本列表 = [
                "福满乾坤喜盈门，春临江户瑞盈门",
                "春回大地千山秀，福照人间万户安",
                "喜居宝地千年旺，福照家门万事兴",
                "春风送暖入屠苏，福雨滋润沃千家"
            ]
            春联 = random.choice(春联文本列表)
            if self.节日系统.添加春联(春联):
                self.界面.显示文本(f"收集到新春联：{春联}")
        
        self.界面.等待按键()
    
    def 时间推进(self):
        """推进游戏时间"""
        选项 = ["前进一天", "前进一周", "前进一个月", "直接到下一年", "返回"]
        选择 = self.界面.输入选择(选项, "时间推进方式:")
        
        if 选择 == 0:  # 前进一天
            self.当前日期 += datetime.timedelta(days=1)
            self.界面.显示文本(f"时间推进到: {self.当前日期.year}年{self.当前日期.month}月{self.当前日期.day}日")
        elif 选择 == 1:  # 前进一周
            self.当前日期 += datetime.timedelta(days=7)
            self.界面.显示文本(f"时间推进到: {self.当前日期.year}年{self.当前日期.month}月{self.当前日期.day}日")
        elif 选择 == 2:  # 前进一个月
            新月份 = self.当前日期.month + 1
            新年份 = self.当前日期.year
            if 新月份 > 12:
                新月份 = 1
                新年份 += 1
            
            # 处理月份天数问题
            try:
                self.当前日期 = datetime.date(新年份, 新月份, self.当前日期.day)
            except ValueError:
                # 如果日期无效（例如2月30日），则使用月末日期
                if 新月份 == 2:
                    self.当前日期 = datetime.date(新年份, 新月份, 28)
                else:
                    self.当前日期 = datetime.date(新年份, 新月份, 30)
            
            self.界面.显示文本(f"时间推进到: {self.当前日期.year}年{self.当前日期.month}月{self.当前日期.day}日")
        elif 选择 == 3:  # 直接到下一年
            if self.玩家.时间推进():
                self.当前日期 = datetime.date(self.玩家.当前年份, 1, 1)
                self.界面.显示时间推进(self.玩家.当前年份, self.玩家.当前章节)
                
                # 检查是否触发年份事件
                事件列表 = events_data.获取年份事件(self.玩家.当前年份)
                未触发事件 = self.玩家.获取未触发事件(事件列表)
                
                if 未触发事件:
                    # 80%概率触发年度事件
                    if random.random() < 0.8:
                        事件名 = random.choice(未触发事件)
                        self.触发事件(事件名)
            else:
                self.界面.显示文本("你已经到达了游戏的最后一年。")
                
        elif 选择 == 4:  # 返回
            return
            
        # 检查年份是否需要变更
        if self.当前日期.year != self.玩家.当前年份:
            # 判断是否超过游戏结束年份
            if self.当前日期.year > config.ENDING_YEAR:
                self.界面.显示文本("你已经到达了游戏的最后一年。")
                self.当前日期 = datetime.date(config.ENDING_YEAR, 12, 31)
            else:
                # 更新玩家年份
                原年份 = self.玩家.当前年份
                while self.玩家.当前年份 < self.当前日期.year:
                    self.玩家.时间推进()
                
                self.界面.显示时间推进(self.玩家.当前年份, self.玩家.当前章节)
                
                # 可能触发年度事件(只在刚好跨年时触发)
                if 原年份 + 1 == self.玩家.当前年份:
                    事件列表 = events_data.获取年份事件(self.玩家.当前年份)
                    未触发事件 = self.玩家.获取未触发事件(事件列表)
                    
                    if 未触发事件 and random.random() < 0.8:
                        事件名 = random.choice(未触发事件)
                        self.触发事件(事件名)
        
        self.界面.等待按键()
    
    def 显示节日收藏(self):
        """显示节日收藏品和记录"""
        # 获取各类节日数据
        收藏的春联 = self.节日系统.获取收集的春联()
        压岁钱记录 = self.节日系统.获取压岁钱记录()
        拜年记录 = self.节日系统.获取拜年记录()
        节日物品 = self.节日系统.获取节日物品()
        
        # 构建显示内容
        内容 = "【节日收藏与记录】\n\n"
        
        # 显示收集的春联
        内容 += "收集的春联:\n"
        if 收藏的春联:
            for i, 春联 in enumerate(收藏的春联, 1):
                内容 += f"{i}. {春联}\n"
        else:
            内容 += "暂无收集的春联\n"
            
        内容 += "\n压岁钱记录:\n"
        if 压岁钱记录:
            总金额 = 0
            for 年份, 金额 in 压岁钱记录.items():
                内容 += f"{年份}年: {金额}元\n"
                总金额 += int(金额)
            内容 += f"累计: {总金额}元\n"
        else:
            内容 += "暂无压岁钱记录\n"
            
        内容 += "\n拜年记录:\n"
        if 拜年记录:
            for 年份, 对象列表 in 拜年记录.items():
                内容 += f"{年份}年拜访: {', '.join(对象列表)}\n"
        else:
            内容 += "暂无拜年记录\n"
            
        内容 += "\n节日特殊物品:\n"
        if 节日物品:
            for i, 物品 in enumerate(节日物品, 1):
                内容 += f"{i}. {物品}\n"
        else:
            内容 += "暂无节日特殊物品\n"
            
        # 显示习俗
        习俗列表 = self.节日系统.获取区域习俗()
        内容 += f"\n{self.节日系统.当前区域}地区春节习俗:\n"
        for 习俗 in 习俗列表:
            内容 += f"· {习俗}\n"
            
        # 显示信息
        self.界面.显示文本(内容)
        self.界面.等待按键()
            
    def 检查随机事件(self):
        """检查是否触发随机事件
        
        根据当前时间和季节，决定是否触发随机事件
        
        Returns:
            bool: 是否触发了随机事件
        """
        # 获取当前季节
        月份 = self.当前日期.month
        if 3 <= 月份 <= 5:
            季节 = '春'
        elif 6 <= 月份 <= 8:
            季节 = '夏'
        elif 9 <= 月份 <= 11:
            季节 = '秋'
        else:
            季节 = '冬'
            
        # 获取当前年代
        年代 = self.确定当前年代()
        
        # 生成噪声值（0-1之间的随机值，但有一定的连续性）
        日期数值 = self.当前日期.toordinal()
        噪声值 = abs(math.sin(日期数值 * 0.1 + self.random_event_system.noise_seed)) 
        
        # 确定阈值（基础阈值加上季节修正）
        阈值 = self.random_event_system.threshold
        
        # 如果噪声值超过阈值，则触发随机事件
        if 噪声值 > 阈值 and random.random() < 0.3:  # 30%概率检查通过时触发
            return self.触发随机事件(年代, 季节)
        
        return False
    
    def 触发随机事件(self, 年代, 季节):
        """触发随机事件
        
        参数:
            年代(str): 当前年代范围，如'1996-2000'
            季节(str): 当前季节，如'春','夏','秋','冬'
            
        Returns:
            bool: 是否成功触发事件
        """
        # 获取适合当前年代和季节的事件
        可用事件列表 = self.random_event_system.get_suitable_events(年代, 季节, self.玩家)
        
        if not 可用事件列表:
            return False
            
        # 随机选择一个事件
        事件 = random.choice(可用事件列表)
        
        # 显示事件信息
        self.界面.显示文本(f"【{事件['title']}】\n{事件['description']}")
        
        # 如果事件有选项，则显示选项
        if '选项' in 事件 and 事件['选项']:
            选项列表 = [选项['text'] for 选项 in 事件['选项']]
            选择索引 = self.界面.输入选择(选项列表, "你的选择是:")
            选择结果 = 事件['选项'][选择索引]
            
            # 显示选择结果
            self.界面.显示事件结果(选择结果['outcome'])
            
            # 应用选择效果
            self.应用事件效果(选择结果.get('attribute_changes', {}))
        else:
            # 应用默认效果
            self.应用事件效果(事件.get('effects', {}))
            
        # 添加到已触发事件
        self.random_event_system.triggered_events.add(事件['id'])
        
        # 检查是否有收藏品
        if '收藏品' in 事件:
            for 收藏品 in 事件['收藏品']:
                if self.玩家.添加收藏品(收藏品):
                    self.界面.显示文本(f"获得收藏品: {收藏品}")
        
        self.界面.等待按键()
        return True
    
    def 应用事件效果(self, 效果字典):
        """应用事件效果
        
        参数:
            效果字典(dict): 包含属性变化的字典，如{'健康': -10, '金钱': -20}
        """
        for 属性名, 变化值 in 效果字典.items():
            变化信息 = self.玩家.属性变化(属性名, 变化值)
            if 变化信息:
                描述, 数值, 当前值 = 变化信息
                self.界面.显示属性变化(属性名, 描述, 数值, 当前值)
    
    def 处理事件选择(self, 事件, 选择索引):
        """处理事件选择
        
        参数:
            事件(dict): 事件数据
            选择索引(int): 玩家选择的选项索引
            
        Returns:
            dict: 选择结果
        """
        if '选项' not in 事件 or 选择索引 >= len(事件['选项']):
            return {}
            
        return 事件['选项'][选择索引]
    
    def 确定当前年代(self):
        """确定当前年代区间
        
        Returns:
            str: 年代区间，如'1996-2000'
        """
        年份 = self.当前日期.year
        
        if 1996 <= 年份 <= 2000:
            return '1996-2000'
        elif 2001 <= 年份 <= 2005:
            return '2001-2005'
        elif 2006 <= 年份 <= 2010:
            return '2006-2010'
        else:
            return '2001-2005'  # 默认年代
    
    def 启动游戏(self):
        """启动游戏，显示开始菜单"""
        if self.使用图形界面:
            # 图形界面模式下直接开始运行
            self.界面.运行()
        else:
            # 文本界面模式下的原有逻辑
            while True:
                self.界面.显示标题()
                选项 = ["开始新游戏", "加载游戏", "退出"]
                选择 = self.界面.输入选择(选项, "请选择:")
                
                if 选择 == 0:  # 开始新游戏
                    self.开始新游戏()
                elif 选择 == 1:  # 加载游戏
                    self.加载游戏()
                elif 选择 == 2:  # 退出
                    self.界面.显示文本("感谢使用《九零后时光机》！", 1)
                    break
    
    def 处理界面回调(self, 选择):
        """处理图形界面的按钮回调
        
        参数:
            选择: 按钮选项索引
        """
        if self.玩家 is None:
            # 处理开始菜单的选择
            if 选择 == 0:  # 开始新游戏
                self.开始新游戏()
            elif 选择 == 1:  # 加载游戏
                self.加载游戏() 
            elif 选择 == 2:  # 退出游戏
                self.界面.运行中 = False
                sys.exit(0)
        else:
            # 处理主菜单的选择
            if 选择 == 0:  # 探索当前时间
                self.探索当前时间()
            elif 选择 == 1:  # 查看个人属性
                self.界面.显示属性(self.玩家.获取所有属性())
            elif 选择 == 2:  # 查看收藏品
                self.界面.显示收藏品(self.玩家.获取收藏品列表())
            elif 选择 == 3:  # 时间推进
                self.时间推进()
            elif 选择 == 4:  # 保存游戏
                self.保存游戏() 
            elif 选择 == 5:  # 退出游戏
                self.运行中 = False
                self.界面.运行中 = False
                sys.exit(0)
    
    def 获取玩家信息(self):
        """获取玩家基本信息用于界面显示
        
        返回:
            dict: 玩家信息字典
        """
        if not self.玩家:
            return None
            
        年龄 = self.玩家.当前年份 - config.BIRTH_YEAR
        
        return {
            "名字": self.玩家.名字,
            "当前年份": self.玩家.当前年份,
            "当前章节": self.玩家.当前章节,
            "年龄": 年龄,
            "收藏品数量": len(self.玩家.收藏品),
            "已触发事件数": len(self.玩家.已触发事件)
        } 