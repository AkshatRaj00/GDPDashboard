import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import numpy as np
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="🚀 Ultimate GDP Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tesla-style futuristic CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    * {
        font-family: 'Orbitron', monospace !important;
    }
    
    .main {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f3460 100%);
        color: #00ff88;
        animation: backgroundShift 10s ease-in-out infinite;
    }
    
    @keyframes backgroundShift {
        0%, 100% { background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f3460 100%); }
        50% { background: linear-gradient(135deg, #0f3460 0%, #16213e 25%, #1a1a2e 50%, #0a0a0a 100%); }
    }
    
    .main-header {
        background: linear-gradient(45deg, #ff6b35, #f7931e, #ffd23f, #00ff88);
        background-size: 400% 400%;
        animation: gradientShift 3s ease infinite;
        text-align: center;
        padding: 3rem 0;
        border-radius: 25px;
        margin-bottom: 2rem;
        border: 3px solid #00ff88;
        box-shadow: 0 0 50px rgba(0, 255, 136, 0.6), inset 0 0 50px rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        animation: shine 2s infinite;
    }
    
    @keyframes shine {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .main-header h1 {
        font-size: 4rem !important;
        font-weight: 900 !important;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.8);
        margin: 0 !important;
        background: linear-gradient(45deg, #ffffff, #00ff88, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-header p {
        font-size: 1.5rem !important;
        margin: 1rem 0 0 0 !important;
        color: #ffffff !important;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.8);
    }
    
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        border: 2px solid #00ff88;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 
            0 0 30px rgba(0, 255, 136, 0.3),
            inset 0 0 30px rgba(0, 255, 136, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        min-width: 200px;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 136, 0.2), transparent);
        animation: scan 2s infinite;
    }
    
    @keyframes scan {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        box-shadow: 
            0 0 50px rgba(0, 255, 136, 0.6),
            inset 0 0 50px rgba(0, 255, 136, 0.2);
    }
    
    .metric-title {
        font-size: 1.2rem !important;
        color: #00ff88 !important;
        margin-bottom: 1rem !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .metric-value {
        font-size: 3rem !important;
        font-weight: 900 !important;
        color: #ffffff !important;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.8);
        margin: 0 !important;
    }
    
    .chart-container {
        background: linear-gradient(145deg, #0f1419, #1a1a2e);
        border: 2px solid #00ff88;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 
            0 0 30px rgba(0, 255, 136, 0.3),
            inset 0 0 30px rgba(0, 255, 136, 0.05);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(145deg, #0a0a0a, #1a1a2e);
        border-right: 3px solid #00ff88;
    }
    
    .stSelectbox > div > div {
        background: linear-gradient(145deg, #1a1a2e, #16213e) !important;
        border: 2px solid #00ff88 !important;
        border-radius: 10px !important;
        color: #00ff88 !important;
    }
    
    .stMultiSelect > div > div {
        background: linear-gradient(145deg, #1a1a2e, #16213e) !important;
        border: 2px solid #00ff88 !important;
        border-radius: 10px !important;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #00ff88, #00cc6a) !important;
        border: none !important;
        border-radius: 15px !important;
        color: #000000 !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.8) !important;
    }
    
    .sidebar-title {
        font-size: 1.5rem !important;
        color: #00ff88 !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
        text-transform: uppercase !important;
        letter-spacing: 3px !important;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.8) !important;
    }
    
    .data-table {
        background: linear-gradient(145deg, #0f1419, #1a1a2e) !important;
        border: 2px solid #00ff88 !important;
        border-radius: 15px !important;
        color: #00ff88 !important;
    }
    
    .status-online {
        color: #00ff88;
        font-weight: bold;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .loading-text {
        font-size: 1.5rem;
        color: #00ff88;
        text-align: center;
        animation: loading 1.5s infinite;
    }
    
    @keyframes loading {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    .feature-highlight {
        background: linear-gradient(45deg, #ff6b35, #00ff88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    .country-flag {
        width: 30px;
        height: 20px;
        margin-right: 10px;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# Country flags mapping (using flag emojis)
COUNTRY_FLAGS = {
    'United States': '🇺🇸', 'China': '🇨🇳', 'Japan': '🇯🇵', 'Germany': '🇩🇪', 
    'United Kingdom': '🇬🇧', 'India': '🇮🇳', 'France': '🇫🇷', 'Italy': '🇮🇹',
    'Brazil': '🇧🇷', 'Canada': '🇨🇦', 'Russia': '🇷🇺', 'South Korea': '🇰🇷',
    'Australia': '🇦🇺', 'Spain': '🇪🇸', 'Mexico': '🇲🇽', 'Indonesia': '🇮🇩',
    'Netherlands': '🇳🇱', 'Saudi Arabia': '🇸🇦', 'Turkey': '🇹🇷', 'Taiwan': '🇹🇼',
    'Belgium': '🇧🇪', 'Argentina': '🇦🇷', 'Sweden': '🇸🇪', 'Poland': '🇵🇱',
    'Ireland': '🇮🇪', 'Israel': '🇮🇱', 'Norway': '🇳🇴', 'Egypt': '🇪🇬',
    'South Africa': '🇿🇦', 'Philippines': '🇵🇭', 'Bangladesh': '🇧🇩', 'Chile': '🇨🇱',
    'Finland': '🇫🇮', 'Romania': '🇷🇴', 'Czech Republic': '🇨🇿', 'New Zealand': '🇳🇿',
    'Peru': '🇵🇪', 'Vietnam': '🇻🇳', 'Portugal': '🇵🇹', 'Greece': '🇬🇷'
}

@st.cache_data(ttl=3600)
def load_ultimate_gdp_data():
    """Load ultimate GDP data with Tesla-level sophistication"""
    
    # Enhanced realistic data with more countries and better patterns
    countries_data = {
        'United States': {'base': 25000, 'growth': 0.025, 'volatility': 0.02},
        'China': {'base': 18000, 'growth': 0.065, 'volatility': 0.03},
        'Japan': {'base': 5200, 'growth': 0.008, 'volatility': 0.015},
        'Germany': {'base': 4500, 'growth': 0.015, 'volatility': 0.02},
        'United Kingdom': {'base': 3300, 'growth': 0.012, 'volatility': 0.025},
        'India': {'base': 3700, 'growth': 0.068, 'volatility': 0.04},
        'France': {'base': 3000, 'growth': 0.013, 'volatility': 0.02},
        'Italy': {'base': 2200, 'growth': 0.005, 'volatility': 0.025},
        'Brazil': {'base': 2100, 'growth': 0.008, 'volatility': 0.035},
        'Canada': {'base': 2000, 'growth': 0.018, 'volatility': 0.02},
        'Russia': {'base': 1900, 'growth': 0.015, 'volatility': 0.045},
        'South Korea': {'base': 1900, 'growth': 0.025, 'volatility': 0.03},
        'Australia': {'base': 1600, 'growth': 0.022, 'volatility': 0.025},
        'Spain': {'base': 1500, 'growth': 0.01, 'volatility': 0.03},
        'Mexico': {'base': 1400, 'growth': 0.015, 'volatility': 0.03},
        'Indonesia': {'base': 1300, 'growth': 0.045, 'volatility': 0.035},
        'Netherlands': {'base': 1000, 'growth': 0.018, 'volatility': 0.02},
        'Saudi Arabia': {'base': 850, 'growth': 0.02, 'volatility': 0.04},
        'Turkey': {'base': 800, 'growth': 0.035, 'volatility': 0.05},
        'Taiwan': {'base': 750, 'growth': 0.025, 'volatility': 0.025},
    }
    
    # Generate sophisticated time series data
    np.random.seed(42)
    data = []
    
    for country, params in countries_data.items():
        base_gdp = params['base']
        trend_growth = params['growth']
        volatility = params['volatility']
        
        for year in range(2000, 2024):
            # Complex growth modeling
            age = year - 2000
            
            # Economic cycles (7-year cycles)
            cycle_factor = 0.01 * np.sin(2 * np.pi * age / 7)
            
            # COVID impact
            covid_impact = 0
            if year == 2020:
                covid_impact = -0.05 + np.random.normal(0, 0.02)
            elif year == 2021:
                covid_impact = 0.03 + np.random.normal(0, 0.015)
            
            # Financial crisis impact
            if year in [2008, 2009]:
                covid_impact = -0.03 + np.random.normal(0, 0.02)
            
            # Calculate GDP with sophisticated modeling
            annual_growth = (
                trend_growth + 
                cycle_factor + 
                covid_impact + 
                np.random.normal(0, volatility)
            )
            
            gdp = base_gdp * ((1 + trend_growth) ** age) * (1 + annual_growth)
            gdp = max(gdp, base_gdp * 0.5)  # Floor value
            
            data.append({
                'Country': country,
                'Country_Code': country[:3].upper(),
                'Year': year,
                'GDP': gdp * 1e9,
                'GDP_Billions': gdp,
                'Growth_Rate': annual_growth * 100,
                'Flag': COUNTRY_FLAGS.get(country, '🏳️')
            })
    
    return pd.DataFrame(data)

def create_tesla_metrics(df, selected_countries, selected_year):
    """Create Tesla-style metrics with advanced calculations"""
    current_data = df[df['Year'] == selected_year]
    
    if selected_countries:
        current_data = current_data[current_data['Country'].isin(selected_countries)]
    
    total_gdp = current_data['GDP_Billions'].sum()
    avg_gdp = current_data['GDP_Billions'].mean()
    max_gdp = current_data['GDP_Billions'].max()
    
    # Advanced growth calculation
    prev_year_data = df[df['Year'] == (selected_year - 1)]
    if selected_countries:
        prev_year_data = prev_year_data[prev_year_data['Country'].isin(selected_countries)]
    
    if not prev_year_data.empty:
        prev_total = prev_year_data['GDP_Billions'].sum()
        growth_rate = ((total_gdp - prev_total) / prev_total * 100) if prev_total > 0 else 0
    else:
        growth_rate = 0
    
    # Market dominance (largest economy share)
    market_share = (max_gdp / total_gdp * 100) if total_gdp > 0 else 0
    
    return total_gdp, avg_gdp, growth_rate, market_share, len(current_data)

def create_ultimate_comparison_chart(df, selected_countries, selected_year):
    """Create ultimate Tesla-style comparison chart"""
    data = df[(df['Year'] == selected_year) & (df['Country'].isin(selected_countries))]
    data = data.sort_values('GDP_Billions', ascending=True)
    
    # Create country labels with flags
    data['Country_Display'] = data.apply(lambda x: f"{x['Flag']} {x['Country']}", axis=1)
    
    fig = go.Figure()
    
    # Add main bars with gradient effect
    fig.add_trace(go.Bar(
        x=data['GDP_Billions'],
        y=data['Country_Display'],
        orientation='h',
        marker=dict(
            color=data['GDP_Billions'],
            colorscale='viridis',
            colorbar=dict(title="GDP (Billions USD)"),
            line=dict(color='#00ff88', width=2)
        ),
        text=data['GDP_Billions'].apply(lambda x: f'${x:,.0f}B'),
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>GDP: $%{x:,.0f}B<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text=f'🚀 GDP POWER RANKINGS - {selected_year}',
            font=dict(size=24, color='#00ff88', family='Orbitron'),
            x=0.5
        ),
        xaxis_title='GDP (Billions USD)',
        yaxis_title='Countries',
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00ff88', family='Orbitron'),
        xaxis=dict(gridcolor='rgba(0, 255, 136, 0.2)'),
        yaxis=dict(gridcolor='rgba(0, 255, 136, 0.2)')
    )
    
    return fig

def create_tesla_trend_chart(df, selected_countries):
    """Create Tesla-style futuristic trend chart"""
    filtered_df = df[df['Country'].isin(selected_countries)]
    
    fig = go.Figure()
    
    colors = px.colors.qualitative.Set3
    
    for i, country in enumerate(selected_countries):
        country_data = filtered_df[filtered_df['Country'] == country]
        flag = COUNTRY_FLAGS.get(country, '🏳️')
        
        fig.add_trace(go.Scatter(
            x=country_data['Year'],
            y=country_data['GDP_Billions'],
            mode='lines+markers',
            name=f'{flag} {country}',
            line=dict(width=4, color=colors[i % len(colors)]),
            marker=dict(size=8, line=dict(width=2, color='white')),
            hovertemplate=f'<b>{flag} {country}</b><br>Year: %{{x}}<br>GDP: $%{{y:,.0f}}B<extra></extra>'
        ))
    
    fig.update_layout(
        title=dict(
            text='🌟 GDP EVOLUTION TIMELINE',
            font=dict(size=24, color='#00ff88', family='Orbitron'),
            x=0.5
        ),
        xaxis_title='Year',
        yaxis_title='GDP (Billions USD)',
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00ff88', family='Orbitron'),
        xaxis=dict(gridcolor='rgba(0, 255, 136, 0.2)'),
        yaxis=dict(gridcolor='rgba(0, 255, 136, 0.2)'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_tesla_growth_heatmap(df, selected_countries):
    """Create Tesla-style growth heatmap"""
    growth_data = []
    
    for country in selected_countries:
        country_data = df[df['Country'] == country].sort_values('Year')
        flag = COUNTRY_FLAGS.get(country, '🏳️')
        
        for i in range(1, len(country_data)):
            current_gdp = country_data.iloc[i]['GDP_Billions']
            prev_gdp = country_data.iloc[i-1]['GDP_Billions']
            growth_rate = ((current_gdp - prev_gdp) / prev_gdp) * 100
            
            growth_data.append({
                'Country': f'{flag} {country}',
                'Year': country_data.iloc[i]['Year'],
                'Growth_Rate': growth_rate
            })
    
    growth_df = pd.DataFrame(growth_data)
    
    # Create pivot table for heatmap
    pivot_df = growth_df.pivot(index='Country', columns='Year', values='Growth_Rate')
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        colorscale='RdYlGn',
        colorbar=dict(title="Growth Rate (%)"),
        hoverongaps=False,
        hovertemplate='<b>%{y}</b><br>Year: %{x}<br>Growth: %{z:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='🔥 GROWTH RATE HEATMAP',
            font=dict(size=24, color='#00ff88', family='Orbitron'),
            x=0.5
        ),
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00ff88', family='Orbitron')
    )
    
    return fig

def create_tesla_pie_chart(df, selected_countries, selected_year):
    """Create Tesla-style futuristic pie chart"""
    data = df[(df['Year'] == selected_year) & (df['Country'].isin(selected_countries))]
    
    # Create labels with flags
    data['Country_Display'] = data.apply(lambda x: f"{x['Flag']} {x['Country']}", axis=1)
    
    fig = go.Figure(data=[go.Pie(
        labels=data['Country_Display'],
        values=data['GDP_Billions'],
        hole=0.4,
        marker=dict(
            colors=px.colors.qualitative.Set3,
            line=dict(color='#00ff88', width=3)
        ),
        textinfo='label+percent',
        textfont=dict(size=12, color='white'),
        hovertemplate='<b>%{label}</b><br>GDP: $%{value:,.0f}B<br>Share: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(
            text=f'💎 MARKET SHARE - {selected_year}',
            font=dict(size=24, color='#00ff88', family='Orbitron'),
            x=0.5
        ),
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00ff88', family='Orbitron'),
        annotations=[dict(text=f'{selected_year}', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    
    return fig

def create_3d_surface_plot(df, selected_countries):
    """Create mind-blowing 3D surface plot"""
    # Prepare data for 3D plot
    pivot_data = df[df['Country'].isin(selected_countries[:5])]  # Limit for performance
    
    z_data = []
    countries_subset = selected_countries[:5]
    years = sorted(df['Year'].unique())
    
    for country in countries_subset:
        country_data = df[df['Country'] == country].sort_values('Year')
        gdp_values = []
        for year in years:
            year_data = country_data[country_data['Year'] == year]
            if not year_data.empty:
                gdp_values.append(year_data['GDP_Billions'].iloc[0])
            else:
                gdp_values.append(0)
        z_data.append(gdp_values)
    
    fig = go.Figure(data=[go.Surface(
        z=z_data,
        x=years,
        y=countries_subset,
        colorscale='viridis',
        showscale=True
    )])
    
    fig.update_layout(
        title=dict(
            text='🌌 3D GDP UNIVERSE',
            font=dict(size=24, color='#00ff88', family='Orbitron'),
            x=0.5
        ),
        scene=dict(
            xaxis_title='Year',
            yaxis_title='Countries',
            zaxis_title='GDP (Billions)',
            bgcolor='rgba(0,0,0,0.8)'
        ),
        height=600,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00ff88', family='Orbitron')
    )
    
    return fig

# Main Tesla-style app
def main():
    # Epic header with animations
    st.markdown("""
    <div class="main-header">
        <h1>🚀 ULTIMATE GDP DASHBOARD</h1>
        <p>⚡ Tesla-Level Analytics • World Domination Edition ⚡</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Loading animation
    loading_container = st.empty()
    with loading_container:
        st.markdown('<div class="loading-text">🔄 Initializing Quantum GDP Matrix...</div>', unsafe_allow_html=True)
        time.sleep(1)
        st.markdown('<div class="loading-text">⚡ Connecting to Global Financial Grid...</div>', unsafe_allow_html=True)
        time.sleep(1)
        st.markdown('<div class="loading-text">🌍 Loading World Economic Data...</div>', unsafe_allow_html=True)
        time.sleep(1)
    loading_container.empty()
    
    # Load ultimate data
    df = load_ultimate_gdp_data()
    
    # Sidebar with Tesla styling
    st.sidebar.markdown('<div class="sidebar-title">🎛️ CONTROL PANEL</div>', unsafe_allow_html=True)
    
    # Real-time status
    st.sidebar.markdown('<div class="status-online">🟢 SYSTEM ONLINE</div>', unsafe_allow_html=True)
    st.sidebar.markdown(f'<div class="status-online">📡 Data Points: {len(df):,}</div>', unsafe_allow_html=True)
    
    # Enhanced country selection with flags
    available_countries = sorted(df['Country'].unique())
    country_options = [f"{COUNTRY_FLAGS.get(country, '🏳️')} {country}" for country in available_countries]
    
    selected_display = st.sidebar.multiselect(
        "🌍 SELECT NATIONS",
        options=country_options,
        default=country_options[:7],  # Top 7 countries
        help="Choose countries for ultimate analysis"
    )
    
    # Extract actual country names
    selected_countries = [option.split(' ', 1)[1] for option in selected_display]
    
    # Year selection
    available_years = sorted(df['Year'].unique())
    selected_year = st.sidebar.selectbox(
        "📅 TIME SELECTOR",
        options=available_years,
        index=len(available_years)-1,
        help="Choose year for temporal analysis"
    )
    
    # Analysis mode
    analysis_mode = st.sidebar.selectbox(
        "🧠 ANALYSIS MODE",
        options=["Standard", "Advanced", "God Mode"],
        index=2,
        help="Select analysis complexity level"
    )
    
    if not selected_countries:
        st.warning("⚠️ Please select nations to unlock the matrix!")
        return
    
    # Calculate Tesla metrics
    total_gdp, avg_gdp, growth_rate, market_share, country_count = create_tesla_metrics(df, selected_countries, selected_year)
    
    # Ultimate metrics display
    st.markdown("## 📊 QUANTUM METRICS")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">💰 TOTAL POWER</div>
            <div class="metric-value">${total_gdp:,.0f}B</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">⚡ AVERAGE FORCE</div>
            <div class="metric-value">${avg_gdp:,.0f}B</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        color = "#00ff88" if growth_rate >= 0 else "#ff4444"
        arrow = "🚀" if growth_rate >= 0 else "📉"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">📈 GROWTH VELOCITY</div>
            <div class="metric-value" style="color: {color}">{arrow} {growth_rate:+.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">👑 DOMINANCE</div>
            <div class="metric-value">{market_share:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🌍 NATIONS</div>
            <div class="metric-value">{country_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Live updates simulation
    st.markdown("---")
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(100):
        progress_bar.progress(i + 1)
        if i < 30:
            status_text.text('🔄 Analyzing market dynamics...')
        elif i < 60:
            status_text.text('⚡ Processing quantum calculations...')
        elif i < 90:
            status_text.text('🚀 Generating Tesla-level insights...')
        else:
            status_text.text('✅ Analysis complete! Ready to dominate!')
        time.sleep(0.01)
    
    progress_bar.empty()
    status_text.empty()
    
    # Ultimate charts section
    st.markdown("## 🎯 VISUAL DOMINANCE CENTER")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏆 POWER RANKINGS", "📈 TIME MACHINE", "🔥 GROWTH MATRIX", "💎 MARKET SHARE", "🌌 3D UNIVERSE"])
    
    with tab1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_comparison = create_ultimate_comparison_chart(df, selected_countries, selected_year)
        st.plotly_chart(fig_comparison, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Top performer highlight
        current_data = df[(df['Year'] == selected_year) & (df['Country'].isin(selected_countries))]
        top_performer = current_data.loc[current_data['GDP_Billions'].idxmax()]
        st.markdown(f"""
        <div style="text-align: center; margin: 2rem 0;">
            <h3 class="feature-highlight">🏆 ECONOMIC CHAMPION: {COUNTRY_FLAGS.get(top_performer['Country'], '🏳️')} {top_performer['Country']}</h3>
            <p style="color: #00ff88; font-size: 1.2rem;">Dominating with ${top_performer['GDP_Billions']:,.0f}B in economic firepower!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_trend = create_tesla_trend_chart(df, selected_countries)
        st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Historical insights
        st.markdown("### 🎯 HISTORICAL INSIGHTS")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📊 Fastest Growing Nation:**")
            # Calculate average growth
            growth_rates = {}
            for country in selected_countries:
                country_data = df[df['Country'] == country].sort_values('Year')
                if len(country_data) > 1:
                    first_year = country_data.iloc[0]['GDP_Billions']
                    last_year = country_data.iloc[-1]['GDP_Billions']
                    years_span = country_data.iloc[-1]['Year'] - country_data.iloc[0]['Year']
                    avg_growth = ((last_year / first_year) ** (1/years_span) - 1) * 100
                    growth_rates[country] = avg_growth
            
            if growth_rates:
                fastest_growing = max(growth_rates.keys(), key=lambda k: growth_rates[k])
                st.markdown(f"🚀 **{COUNTRY_FLAGS.get(fastest_growing, '🏳️')} {fastest_growing}** ({growth_rates[fastest_growing]:.1f}% annually)")
        
        with col2:
            st.markdown("**💪 Most Stable Economy:**")
            # Calculate volatility (standard deviation of growth rates)
            volatilities = {}
            for country in selected_countries:
                country_data = df[df['Country'] == country].sort_values('Year')
                if len(country_data) > 2:
                    growth_series = country_data['GDP_Billions'].pct_change().dropna()
                    volatility = growth_series.std() * 100
                    volatilities[country] = volatility
            
            if volatilities:
                most_stable = min(volatilities.keys(), key=lambda k: volatilities[k])
                st.markdown(f"⚖️ **{COUNTRY_FLAGS.get(most_stable, '🏳️')} {most_stable}** ({volatilities[most_stable]:.1f}% volatility)")
    
    with tab3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_heatmap = create_tesla_growth_heatmap(df, selected_countries)
        st.plotly_chart(fig_heatmap, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Growth analysis
        st.markdown("### 🔥 GROWTH ANALYSIS")
        recent_growth = df[df['Year'] == selected_year]['Growth_Rate'].mean()
        st.markdown(f"""
        <div style="text-align: center;">
            <h3 style="color: #00ff88;">Global Average Growth Rate: {recent_growth:.1f}%</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_pie = create_tesla_pie_chart(df, selected_countries, selected_year)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Market concentration
        current_data = df[(df['Year'] == selected_year) & (df['Country'].isin(selected_countries))]
        total = current_data['GDP_Billions'].sum()
        top_3_share = current_data.nlargest(3, 'GDP_Billions')['GDP_Billions'].sum() / total * 100
        
        st.markdown(f"""
        <div style="text-align: center; margin: 2rem 0;">
            <h3 class="feature-highlight">📊 TOP 3 CONTROL: {top_3_share:.1f}% of Total Economic Power</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with tab5:
        if analysis_mode == "God Mode":
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig_3d = create_3d_surface_plot(df, selected_countries)
            st.plotly_chart(fig_3d, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("### 🌌 MULTIDIMENSIONAL INSIGHTS")
            st.markdown("""
            <div style="color: #00ff88; font-family: 'Orbitron', monospace;">
            🔮 <strong>Quantum Analysis Reveals:</strong><br>
            • Economic trajectories follow complex wave patterns<br>
            • Peak performance correlations detected across temporal dimensions<br>
            • Future growth vectors optimally calculated<br>
            • Market singularities identified in the economic spacetime
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; color: #00ff88; font-size: 1.5rem; margin: 3rem 0;">
                🔒 3D UNIVERSE MODE LOCKED<br>
                <small>Upgrade to "God Mode" to unlock interdimensional analysis</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Ultimate data table
    st.markdown("## 📋 ECONOMIC INTELLIGENCE DATABASE")
    
    # Enhanced data display
    display_data = df[
        (df['Country'].isin(selected_countries)) & 
        (df['Year'] >= selected_year - 4) & 
        (df['Year'] <= selected_year)
    ].sort_values(['Year', 'GDP_Billions'], ascending=[False, False])
    
    # Create enhanced display
    display_enhanced = display_data.copy()
    display_enhanced['Nation'] = display_enhanced.apply(lambda x: f"{x['Flag']} {x['Country']}", axis=1)
    display_enhanced['Economic Power'] = display_enhanced['GDP_Billions'].apply(lambda x: f"${x:,.0f}B")
    display_enhanced['Mega Power'] = display_enhanced['GDP_Billions'].apply(lambda x: f"${x/1000:.2f}T")
    display_enhanced['Growth %'] = display_enhanced['Growth_Rate'].apply(lambda x: f"{x:+.1f}%")
    
    # Rank countries
    for year in display_enhanced['Year'].unique():
        year_data = display_enhanced[display_enhanced['Year'] == year].sort_values('GDP_Billions', ascending=False)
        display_enhanced.loc[display_enhanced['Year'] == year, 'Global Rank'] = range(1, len(year_data) + 1)
    
    st.markdown('<div class="data-table">', unsafe_allow_html=True)
    st.dataframe(
        display_enhanced[['Nation', 'Year', 'Economic Power', 'Mega Power', 'Growth %', 'Global Rank']],
        use_container_width=True,
        height=400
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Ultimate download options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv_data = display_data.to_csv(index=False)
        st.download_button(
            label="📥 DOWNLOAD CSV MATRIX",
            data=csv_data,
            file_name=f'tesla_gdp_matrix_{selected_year}.csv',
            mime='text/csv'
        )
    
    with col2:
        json_data = display_data.to_json(orient='records', indent=2)
        st.download_button(
            label="🔥 DOWNLOAD JSON CORE",
            data=json_data,
            file_name=f'tesla_gdp_core_{selected_year}.json',
            mime='application/json'
        )
    
    with col3:
        # Summary report
        summary = f"""
TESLA-LEVEL GDP ANALYSIS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Analysis Mode: {analysis_mode}

SELECTED NATIONS: {len(selected_countries)}
{', '.join([f"{COUNTRY_FLAGS.get(c, '🏳️')} {c}" for c in selected_countries])}

KEY INSIGHTS FOR {selected_year}:
💰 Total Economic Power: ${total_gdp:,.0f}B
⚡ Average Force: ${avg_gdp:,.0f}B  
📈 Growth Velocity: {growth_rate:+.1f}%
👑 Market Dominance: {market_share:.1f}%

STATUS: ANALYSIS COMPLETE ✅
TESLA APPROVAL: APPROVED 🚀
        """
        
        st.download_button(
            label="🚀 TESLA REPORT",
            data=summary,
            file_name=f'tesla_analysis_report_{selected_year}.txt',
            mime='text/plain'
        )
    
    # Epic footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0;">
        <div style="font-size: 2rem; margin-bottom: 1rem;">
            🚀⚡🌍⚡🚀
        </div>
        <div class="feature-highlight" style="font-size: 1.5rem;">
            ULTIMATE GDP DASHBOARD - TESLA EDITION
        </div>
        <div style="color: #00ff88; margin: 1rem 0; font-family: 'Orbitron', monospace;">
            🔥 World's Most Advanced Economic Intelligence System 🔥<br>
            ⚡ Powered by Quantum Analytics • Built for Domination ⚡<br>
            🌟 Making Economics Look Easy Since 2024 🌟
        </div>
        <div style="color: #666; font-size: 0.9rem;">
            Real-time data synthesis • Tesla-grade performance • Elon Musk approved*<br>
            <small>*Elon approval pending but guaranteed 😎</small>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Secret Easter Egg
    if st.sidebar.button("🔥 ACTIVATE BEAST MODE"):
        st.balloons()
        st.markdown("""
        <div style="text-align: center; color: #ff6b35; font-size: 2rem; animation: pulse 1s infinite;">
            🚀 BEAST MODE ACTIVATED! 🚀<br>
            <span style="font-size: 1rem;">You've unlocked the secret Tesla power-up!</span>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()