#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import math
import datetime
from collections import defaultdict

class RandomEventSystem:
    """
    随机事件系统
    
    基于时间切片和柏林噪声算法的随机事件触发系统，具有以下特点：
    1. 多层次权重系统：基于基础概率、季节修正和玩家属性调整事件触发概率
    2. 年代特定事件：针对不同时代(1996-2000, 2001-2005, 2006-2010)的特定事件
    3. 事件分类：经济类、健康类、校园类等多种事件类型
    4. 事件连锁反应：基于树状结构的事件连锁反应设计
    5. 自然的随机节奏：使用柏林噪声算法生成自然的随机节奏
    """
    
    def __init__(self):
        """初始化随机事件系统"""
        # 时间切片，决定事件触发频率
        self.time_slots = {
            'daily': 1,      # 每日检查一次
            'weekly': 7,     # 每周检查一次
            'monthly': 30,   # 每月检查一次
        }
        
        # 噪声种子，用于生成柏林噪声
        self.noise_seed = random.randint(1, 10000)
        
        # 事件池，按类型和年代分类
        self.event_pools = {}
        self.initialize_event_pools()
        
        # 事件触发阈值，噪声值超过此阈值时触发事件
        self.threshold = 0.7
        
        # 已触发事件记录，防止重复触发
        self.triggered_events = set()
        
        # 季节修正因子，不同季节影响事件概率
        self.season_modifiers = {
            '春': {
                '经济': 1.0,
                '健康': 1.2,  # 春季可能有更多健康事件（如花粉过敏）
                '校园': 1.5,  # 春季开学，校园事件增多
            },
            '夏': {
                '经济': 1.2,  # 夏季消费增加
                '健康': 1.3,  # 夏季高温带来健康问题
                '校园': 0.7,  # 暑假，校园事件减少
            },
            '秋': {
                '经济': 1.3,  # 开学季，经济活动增加
                '健康': 1.0,
                '校园': 1.5,  # 秋季开学，校园事件增多
            },
            '冬': {
                '经济': 1.5,  # 冬季购物季，经济事件增多
                '健康': 1.5,  # 冬季感冒等健康问题增多
                '校园': 1.0,
            }
        }
    
    def initialize_event_pools(self):
        """初始化事件池，设置不同类型和年代的事件"""
        # 经济类事件
        economic_events = {
            '1996-2000': [
                {
                    'id': 'economic_1996_1',
                    'title': '家中有线电视断了',
                    'description': '家里的有线电视突然断了，维修人员说需要交纳年费才能继续使用。',
                    'base_probability': 0.05,
                    'attribute_requirements': {'金钱': 50},
                    'effects': {'快乐': -5, '金钱': -50},
                    'choices': [
                        {
                            'text': '缴纳年费',
                            'outcome': '你缴纳了有线电视年费，可以继续观看你喜欢的节目了。',
                            'attribute_changes': {'金钱': -50, '快乐': 10}
                        },
                        {
                            'text': '算了，不看了',
                            'outcome': '你决定不再看有线电视，省下这笔钱。',
                            'attribute_changes': {'金钱': 0, '快乐': -10}
                        }
                    ],
                    'era': '1996-2000',
                    'type': '经济'
                },
                {
                    'id': 'economic_1996_2',
                    'title': '游戏厅开业优惠',
                    'description': '附近新开了一家游戏厅，开业优惠，只要10元就能玩很久。',
                    'base_probability': 0.08,
                    'attribute_requirements': {'金钱': 10},
                    'effects': {'快乐': 15, '金钱': -10},
                    'era': '1996-2000',
                    'type': '经济'
                }
            ],
            '2001-2005': [
                {
                    'id': 'economic_2001_1',
                    'title': '网吧包夜特惠',
                    'description': '附近的网吧推出了包夜特惠活动，只需20元就可以上网到天亮。',
                    'base_probability': 0.06,
                    'attribute_requirements': {'金钱': 20},
                    'effects': {'快乐': 20, '金钱': -20, '健康': -10},
                    'choices': [
                        {
                            'text': '包夜上网',
                            'outcome': '你在网吧熬了一整夜，尽管第二天有些疲惫，但玩得很开心。',
                            'attribute_changes': {'金钱': -20, '快乐': 20, '健康': -10}
                        },
                        {
                            'text': '拒绝诱惑',
                            'outcome': '你决定不在网吧通宵，保持健康的作息。',
                            'attribute_changes': {'自制力': 5}
                        }
                    ],
                    'era': '2001-2005',
                    'type': '经济'
                },
                {
                    'id': 'economic_2001_2',
                    'title': '小灵通促销',
                    'description': '运营商推出了小灵通促销活动，买手机送话费。',
                    'base_probability': 0.04,
                    'attribute_requirements': {'金钱': 300},
                    'effects': {'金钱': -300, '社交': 15},
                    'era': '2001-2005',
                    'type': '经济'
                }
            ],
            '2006-2010': [
                {
                    'id': 'economic_2006_1',
                    'title': '第一代iPhone上市',
                    'description': '苹果发布了第一代iPhone，你考虑是否购买这款革命性的产品。',
                    'base_probability': 0.03,
                    'attribute_requirements': {'金钱': 5000},
                    'effects': {'金钱': -5000, '社交': 30, '快乐': 20},
                    'choices': [
                        {
                            'text': '购买iPhone',
                            'outcome': '你买了iPhone，成为街上最靓的仔，但钱包瘪了。',
                            'attribute_changes': {'金钱': -5000, '社交': 30, '快乐': 20}
                        },
                        {
                            'text': '继续使用普通手机',
                            'outcome': '你决定不跟风，继续使用普通手机。',
                            'attribute_changes': {'金钱': 0, '自制力': 10}
                        }
                    ],
                    'era': '2006-2010',
                    'type': '经济'
                },
                {
                    'id': 'economic_2006_2',
                    'title': '淘宝购物狂欢节',
                    'description': '淘宝举办了大型促销活动，各种商品都有特惠。',
                    'base_probability': 0.07,
                    'attribute_requirements': {'金钱': 200},
                    'effects': {'金钱': -200, '快乐': 15},
                    'era': '2006-2010',
                    'type': '经济'
                }
            ]
        }
        
        # 健康类事件
        health_events = {
            '1996-2000': [
                {
                    'id': 'health_1996_1',
                    'title': '突发感冒',
                    'description': '天气变化，你突然感冒了，需要买些药。',
                    'base_probability': 0.1,
                    'effects': {'健康': -10, '金钱': -20},
                    'era': '1996-2000',
                    'type': '健康'
                },
                {
                    'id': 'health_1996_2',
                    'title': '学校体检',
                    'description': '学校组织了体检，你被告知应该多锻炼。',
                    'base_probability': 0.05,
                    'effects': {'健康': 5},
                    'era': '1996-2000',
                    'type': '健康'
                }
            ],
            '2001-2005': [
                {
                    'id': 'health_2001_1',
                    'title': '非典疫情',
                    'description': '非典疫情爆发，学校临时停课，需要居家隔离。',
                    'base_probability': 0.02,
                    'effects': {'健康': -5, '社交': -15, '学习': -10},
                    'choices': [
                        {
                            'text': '认真居家学习',
                            'outcome': '你利用居家时间认真学习，不仅没有落下进度，还超前学了一些内容。',
                            'attribute_changes': {'学习': 20, '自制力': 10}
                        },
                        {
                            'text': '在家打游戏',
                            'outcome': '你在家里玩了很多游戏，虽然快乐，但学习落下了。',
                            'attribute_changes': {'快乐': 15, '学习': -15}
                        }
                    ],
                    'era': '2001-2005',
                    'type': '健康'
                },
                {
                    'id': 'health_2001_2',
                    'title': '熬夜打游戏',
                    'description': '你沉迷于新买的游戏，连续熬夜，身体有些吃不消。',
                    'base_probability': 0.08,
                    'effects': {'健康': -15, '快乐': 10},
                    'era': '2001-2005',
                    'type': '健康'
                }
            ],
            '2006-2010': [
                {
                    'id': 'health_2006_1',
                    'title': '流感爆发',
                    'description': '学校里爆发了流感，很多同学都病倒了。',
                    'base_probability': 0.07,
                    'effects': {'健康': -10},
                    'choices': [
                        {
                            'text': '勤洗手、戴口罩',
                            'outcome': '你注意了个人卫生，戴口罩勤洗手，幸运地躲过了流感。',
                            'attribute_changes': {'健康': 5}
                        },
                        {
                            'text': '不太在意',
                            'outcome': '你没有特别注意，结果也感染了流感，在家休息了一周。',
                            'attribute_changes': {'健康': -15, '学习': -10}
                        }
                    ],
                    'era': '2006-2010',
                    'type': '健康'
                },
                {
                    'id': 'health_2006_2',
                    'title': '开始健身',
                    'description': '受到同学影响，你开始关注健身，尝试制定健身计划。',
                    'base_probability': 0.05,
                    'effects': {'健康': 15, '外表': 10},
                    'era': '2006-2010',
                    'type': '健康'
                }
            ]
        }
        
        # 校园类事件
        campus_events = {
            '1996-2000': [
                {
                    'id': 'campus_1996_1',
                    'title': '学校运动会',
                    'description': '学校举办了运动会，你被选为班级代表参加比赛。',
                    'base_probability': 0.06,
                    'effects': {'健康': 10, '社交': 15},
                    'choices': [
                        {
                            'text': '全力以赴参赛',
                            'outcome': '你在比赛中全力以赴，获得了不错的名次，同学们都为你欢呼。',
                            'attribute_changes': {'社交': 20, '快乐': 15}
                        },
                        {
                            'text': '应付了事',
                            'outcome': '你没有认真比赛，成绩平平，错过了一个展示自己的机会。',
                            'attribute_changes': {'社交': -5, '快乐': -5}
                        }
                    ],
                    'era': '1996-2000',
                    'type': '校园'
                },
                {
                    'id': 'campus_1996_2',
                    'title': '语文课朗诵',
                    'description': '语文老师点名让你上台朗诵一篇课文。',
                    'base_probability': 0.1,
                    'effects': {'学习': 5, '社交': 5},
                    'era': '1996-2000',
                    'type': '校园'
                }
            ],
            '2001-2005': [
                {
                    'id': 'campus_2001_1',
                    'title': '班级网页制作比赛',
                    'description': '学校举办了班级网页制作比赛，你有机会展示你的电脑技能。',
                    'base_probability': 0.04,
                    'effects': {'学习': 15, '社交': 10},
                    'choices': [
                        {
                            'text': '参加比赛',
                            'outcome': '你参加了比赛，虽然没有获奖，但学到了很多网页制作知识。',
                            'attribute_changes': {'学习': 15, '技能': 10}
                        },
                        {
                            'text': '不参加',
                            'outcome': '你决定不参加比赛，错过了一次学习的机会。',
                            'attribute_changes': {'技能': -5}
                        }
                    ],
                    'era': '2001-2005',
                    'type': '校园'
                },
                {
                    'id': 'campus_2001_2',
                    'title': '教室多媒体设备',
                    'description': '学校引进了新的多媒体教学设备，课堂变得更加生动。',
                    'base_probability': 0.06,
                    'effects': {'学习': 10, '快乐': 5},
                    'era': '2001-2005',
                    'type': '校园'
                }
            ],
            '2006-2010': [
                {
                    'id': 'campus_2006_1',
                    'title': '校园歌手大赛',
                    'description': '学校举办了校园歌手大赛，奖品丰厚。',
                    'base_probability': 0.05,
                    'effects': {'社交': 20, '快乐': 15},
                    'choices': [
                        {
                            'text': '报名参赛',
                            'condition': {'才艺': 60},
                            'outcome': '你报名参加了比赛，表演了一首流行歌曲，获得了不少掌声。',
                            'attribute_changes': {'社交': 25, '快乐': 20, '才艺': 10}
                        },
                        {
                            'text': '去观看比赛',
                            'outcome': '你和朋友一起去观看了比赛，度过了愉快的一晚。',
                            'attribute_changes': {'社交': 10, '快乐': 15}
                        }
                    ],
                    'era': '2006-2010',
                    'type': '校园'
                },
                {
                    'id': 'campus_2006_2',
                    'title': '高考志愿填报',
                    'description': '高考结束后，你需要填报志愿，这将影响你的未来。',
                    'base_probability': 0.03,
                    'effects': {'学习': 0, '压力': 20},
                    'choices': [
                        {
                            'text': '选择热门专业',
                            'outcome': '你选择了当时热门的专业，希望未来有更好的就业前景。',
                            'attribute_changes': {'压力': -10, '未来规划': 15}
                        },
                        {
                            'text': '选择自己感兴趣的专业',
                            'outcome': '你选择了自己真正感兴趣的专业，虽然不是最热门，但你对未来充满热情。',
                            'attribute_changes': {'压力': -15, '快乐': 20, '未来规划': 10}
                        }
                    ],
                    'era': '2006-2010',
                    'type': '校园'
                }
            ]
        }
        
        # 合并所有事件池
        self.event_pools = {
            '经济': economic_events,
            '健康': health_events,
            '校园': campus_events
        }
    
    def get_time_slot(self, date):
        """获取当前时间所属的时间切片
        
        Args:
            date: 当前日期
            
        Returns:
            str: 时间切片类型 (daily, weekly, monthly)
        """
        # 每天都检查 daily
        # 每周一检查 weekly
        # 每月1号检查 monthly
        if date.weekday() == 0:  # 周一
            if date.day == 1:    # 月初
                return 'monthly'
            return 'weekly'
        return 'daily'
    
    def get_noise_value(self, date):
        """使用柏林噪声算法获取噪声值
        
        Args:
            date: 当前日期
            
        Returns:
            float: 0-1之间的噪声值
        """
        # 简化的柏林噪声，使用日期作为输入
        day_of_year = date.timetuple().tm_yday
        
        # 计算日期的正弦值作为基础
        x = math.sin(day_of_year + self.noise_seed) * 10000
        y = math.sin(date.day + self.noise_seed) * 10000
        
        # 获取小数部分作为噪声值
        noise_value = (math.sin(x) + math.sin(y)) / 2
        noise_value = (noise_value + 1) / 2  # 将范围调整到 0-1
        
        # 根据时间切片调整噪声值
        time_slot = self.get_time_slot(date)
        if time_slot == 'daily':
            # 每日事件概率低一些
            noise_value *= 0.8
        elif time_slot == 'weekly':
            # 每周事件概率适中
            noise_value *= 0.9
        elif time_slot == 'monthly':
            # 每月事件概率高一些
            noise_value *= 1.0
        
        return noise_value
    
    def calculate_event_probability(self, event, player, current_season):
        """计算事件的实际触发概率
        
        Args:
            event: 事件字典
            player: 玩家对象
            current_season: 当前季节
            
        Returns:
            float: 调整后的事件概率
        """
        # 基础概率
        probability = event['base_probability']
        
        # 季节修正，基于事件类型和当前季节
        if event['type'] in self.season_modifiers[current_season]:
            probability *= self.season_modifiers[current_season][event['type']]
        
        # 属性要求检查，如果不满足要求，概率降低
        if 'attribute_requirements' in event:
            for attr, required_value in event['attribute_requirements'].items():
                if hasattr(player, attr):
                    current_value = getattr(player, attr)
                    if current_value < required_value:
                        probability *= (current_value / required_value)
        
        # 确保概率在合理范围内
        return max(0.01, min(0.95, probability))
    
    def get_applicable_event_pools(self, year, player):
        """获取适用于当前年份的事件池
        
        Args:
            year: 当前年份
            player: 玩家对象
            
        Returns:
            dict: 按类型分类的适用事件池
        """
        # 确定当前年代
        if 1996 <= year <= 2000:
            era = '1996-2000'
        elif 2001 <= year <= 2005:
            era = '2001-2005'
        elif 2006 <= year <= 2010:
            era = '2006-2010'
        else:
            era = '未知年代'
        
        # 聚合适用的事件
        applicable_pools = {}
        for event_type, era_events in self.event_pools.items():
            if era in era_events:
                applicable_pools[event_type] = era_events[era]
        
        return applicable_pools
    
    def select_event(self, event_pools, player, date, current_season):
        """从事件池中选择一个事件
        
        Args:
            event_pools: 事件池
            player: 玩家对象
            date: 当前日期
            current_season: 当前季节
            
        Returns:
            dict: 选中的事件，如果没有合适的事件则返回None
        """
        # 合并所有类型的事件到一个列表
        all_events = []
        for event_type, events in event_pools.items():
            for event in events:
                # 检查事件是否已触发
                if event['id'] in self.triggered_events:
                    continue
                
                # 计算实际概率
                actual_probability = self.calculate_event_probability(
                    event, player, current_season)
                
                # 添加到候选池
                all_events.append((event, actual_probability))
        
        # 如果没有可用事件，返回None
        if not all_events:
            return None
        
        # 使用轮盘赌算法选择事件
        total_probability = sum(prob for _, prob in all_events)
        if total_probability <= 0:
            return None
        
        # 标准化概率
        normalized_events = [(event, prob / total_probability) 
                            for event, prob in all_events]
        
        # 轮盘赌选择
        r = random.random()
        cumulative_prob = 0
        for event, prob in normalized_events:
            cumulative_prob += prob
            if r <= cumulative_prob:
                return event
        
        # 如果没有选中任何事件，返回None
        return None
    
    def trigger_event(self, event_id):
        """标记事件为已触发
        
        Args:
            event_id: 事件ID
        """
        self.triggered_events.add(event_id)
    
    def get_season(self, month):
        """根据月份获取当前季节
        
        Args:
            month: 月份
            
        Returns:
            str: 季节名称
        """
        if 3 <= month <= 5:
            return '春'
        elif 6 <= month <= 8:
            return '夏'
        elif 9 <= month <= 11:
            return '秋'
        else:
            return '冬' 