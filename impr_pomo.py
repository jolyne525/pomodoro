import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import random
from datetime import datetime, timedelta
import os

# --- 1. 页面配置 ---
st.set_page_config(page_title="个人专注效率分析系统", page_icon="📊", layout="wide")

# --- 2. 数据层 (Data Layer) ---
DATA_FILE = "focus_history.csv"

def load_data():
    """读取历史数据，如果没有文件则返回空的 DataFrame"""
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["date", "start_time", "duration_minutes", "plant_type", "day_of_week", "hour_of_day"])

def save_record(duration, plant_type):
    """保存一条新的专注记录"""
    now = datetime.now()
    new_data = {
        "date": now.strftime("%Y-%m-%d"),
        "start_time": now.strftime("%H:%M:%S"),
        "duration_minutes": duration,
        "plant_type": plant_type,
        "day_of_week": now.strftime("%A"), # 星期几
        "hour_of_day": now.hour          # 小时 (0-23)
    }
    df = load_data()
    # 使用 pd.concat 替代 append
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    return df

def generate_mock_data():
    """
    改进版数据生成：
    模拟一个“前半个月效率低，后半个月使用系统后效率高”的趋势。
    """
    current_df = load_data()
    if len(current_df) > 50:
        st.warning("数据已存在，建议删除 csv 文件重新生成以查看效果。")
        return

    mock_data = []
    plants = ["🌱 嫩芽", "🌻 向日葵", "🌲 松树", "🌵 仙人掌"]
    days_back = 30 # 模拟过去30天
    
    for i in range(days_back):
        date = datetime.now() - timedelta(days=days_back - i) # 从30天前开始
        day_str = date.strftime("%Y-%m-%d")
        
        # --- 关键修改：制造趋势 ---
        if i < 15: 
            # 前15天 (Before): 每天只专注 1-2 次，每次 25 分钟 (低效)
            sessions = random.randint(1, 2)
            avg_duration = 25
        else:
            # 后15天 (After): 每天专注 4-6 次，每次 45 分钟 (高效)
            sessions = random.randint(4, 6)
            avg_duration = 45
            
        for _ in range(sessions):
            # 模拟随机波动
            duration = int(np.random.normal(avg_duration, 5))
            duration = max(10, duration) # 至少10分钟
            
            # 早上9点到晚上10点之间
            hour = random.randint(9, 22)
            
            mock_data.append({
                "date": day_str,
                "start_time": f"{hour}:00:00",
                "duration_minutes": duration,
                "plant_type": random.choice(plants),
                "day_of_week": date.strftime("%A"),
                "hour_of_day": hour
            })
    
    df = pd.DataFrame(mock_data)
    df.to_csv(DATA_FILE, index=False)
    
    # --- 计算提升率 (用于 CV 展示) ---
    df['period'] = np.where(df.index < len(df)/2, 'Before', 'After')
    avg_before = df[df['period']=='Before']['duration_minutes'].sum() / 15
    avg_after = df[df['period']=='After']['duration_minutes'].sum() / 15
    uplift = (avg_after - avg_before) / avg_before * 100
    
    st.success(f"模拟数据生成完毕！你的日均专注时长提升了 {uplift:.1f}% (CV素材)")
    
# --- 3. 侧边栏：控制区 ---
st.sidebar.title("🎮 控制台")
menu = st.sidebar.radio("导航", ["专注计时器", "数据分析仪表盘"])

st.sidebar.markdown("---")
if st.sidebar.button("生成模拟数据 (测试用)"):
    generate_mock_data()
    st.rerun()

# --- 4. 主界面 ---

if menu == "专注计时器":
    st.title("🍅 专注计时器 (数据采集端)")
    st.caption("每一次专注都会被记录到后台 CSV 数据库中，用于后续分析。")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("⏱️ 当前状态")
        # Session State 初始化
        if 'time_left' not in st.session_state:
            st.session_state.time_left = 25 * 60
        if 'is_running' not in st.session_state:
            st.session_state.is_running = False

        timer_placeholder = st.empty()
        # 简单显示时间
        mins, secs = divmod(st.session_state.time_left, 60)
        timer_placeholder.markdown(f"<h1 style='font-size: 80px;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)

        if st.button("开始专注", type="primary", disabled=st.session_state.is_running):
            st.session_state.is_running = True
            progress_bar = st.progress(0)
            
            # 倒计时逻辑
            total_time = 25 * 60
            while st.session_state.time_left > 0:
                time.sleep(1) # 这里为了演示，如果是真实使用应用 time.sleep(1)
                st.session_state.time_left -= 1
                mins, secs = divmod(st.session_state.time_left, 60)
                timer_placeholder.markdown(f"<h1 style='font-size: 80px;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
                progress_bar.progress((total_time - st.session_state.time_left) / total_time)
            
            # 计时结束
            st.session_state.is_running = False
            st.session_state.time_left = 25 * 60 # 重置
            
            # --- 关键：保存数据 ---
            plant = random.choice(["🌱 嫩芽", "🌻 向日葵", "🌲 松树", "🌵 仙人掌"])
            save_record(25, plant)
            st.balloons()
            st.success(f"数据已上传！本次获得：{plant}")

    with col2:
        st.info("💡 这里的操作逻辑与之前相同，但核心区别在于：所有行为都会被结构化存储。")

elif menu == "数据分析仪表盘":
    st.title("📊 个人效率洞察 (Data Insights)")
    
    df = load_data()
    
    if df.empty:
        st.warning("暂无数据。请先去'专注计时器'完成一次专注，或点击侧边栏的'生成模拟数据'。")
    else:
        # --- 顶部 KPI 指标 ---
        total_sessions = len(df)
        total_hours = round(df['duration_minutes'].sum() / 60, 1)
        fav_time = df['hour_of_day'].mode()[0] if not df.empty else 0
        
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("总专注次数", f"{total_sessions} 次")
        kpi2.metric("累计专注时长", f"{total_hours} 小时")
        kpi3.metric("最佳专注时段", f"{fav_time}:00 - {fav_time+1}:00")
        
        st.divider()

        # --- 图表区 ---
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("📈 每日专注趋势")
            # 按日期分组求和
            daily_trend = df.groupby('date')['duration_minutes'].sum().reset_index()
            fig_trend = px.line(daily_trend, x='date', y='duration_minutes', 
                                title="每日专注时长变化 (Time Series)", markers=True)
            st.plotly_chart(fig_trend, use_container_width=True)
            
        with c2:
            st.subheader("🌹 花园植物分布")
            # 饼图
            plant_counts = df['plant_type'].value_counts().reset_index()
            plant_counts.columns = ['plant_type', 'count']
            fig_pie = px.pie(plant_counts, values='count', names='plant_type', 
                             title="收获植物种类占比 (Distribution)", hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)

        st.subheader("🔥 效率热力图")
        st.caption("分析你在通过一周内不同时段的专注强度，寻找你的'黄金工作时间'。")
        
        # 数据预处理：构建 24小时 x 7天 的矩阵
        heatmap_data = df.groupby(['day_of_week', 'hour_of_day']).size().reset_index(name='count')
        
        # 简单的散点图模拟热力分布 (Bubble Chart)
        fig_heat = px.scatter(heatmap_data, x='hour_of_day', y='day_of_week', size='count', 
                              color='count', color_continuous_scale='Viridis',
                              labels={'hour_of_day': '小时 (0-23)', 'day_of_week': '星期', 'count': '专注次数'},
                              title="专注习惯分布图")
        fig_heat.update_xaxes(range=[0, 24], dtick=1)
        st.plotly_chart(fig_heat, use_container_width=True)

        # --- 原始数据展示 ---
        with st.expander("查看原始数据 (Raw Data)"):
            st.dataframe(df.sort_values(by="date", ascending=False))
