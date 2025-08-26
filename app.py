import streamlit as st
import requests
import plotly.express as px
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.title("UK Company Health Dashboard")
st.write("Enter a company number to see financial health metrics")

# API configuration - Load from environment variable
API_KEY = os.getenv("DATALEDGER_API_KEY")

if not API_KEY:
    st.error("⚠️ DataLedger API key not found. Please add your API key to a .env file:")
    st.code("""
        # Create a .env file in your project directory with:
        DATALEDGER_API_KEY=your_api_key_here
    """)
    st.stop()

company_number = st.text_input("Company Number:", placeholder="e.g. 12345678")

if st.button("Get Company Data") and company_number:
    print(f"DEBUG: Starting API request for company number: {company_number}")
    
    try:
        # Call DataLedger API
        headers = {"x-api-key": API_KEY}
        url = f"https://api.dataledger.uk/v1/companies/{company_number}"
        
        print(f"DEBUG: Making request to URL: {url}")
        
        response = requests.get(url, headers=headers)
        print(f"DEBUG: Response status code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"DEBUG: Successfully retrieved data for company: {data.get('company_name', 'Unknown')}")
            
            # Display company info
            st.header(f"{data.get('companyName', 'Unknown Company')}")
            
            # Extract location from registeredAddress
            registered_address = data.get('registeredAddress', {})
            local_authority = registered_address.get('localAuthority', 'N/A')
            
            # Extract SIC description from industry
            industry = data.get('industry', {})
            sic_description = industry.get('sic1Description', 'N/A')
            
            print(f"DEBUG: Company info - Location: {local_authority}, Employees: {data.get('averageNumberEmployeesDuringPeriod')}")
            st.write(f"**Company Number:** {data.get('companyNumber', 'N/A')}")
            st.write(f"**Status:** {'Active' if data.get('isActive') else 'Inactive'}")
            st.write(f"**Location:** {local_authority}")
            st.write(f"**Employees:** {data.get('averageNumberEmployeesDuringPeriod', 'N/A')}")
            st.write(f"**Primary SIC:** {sic_description}")
            st.write(f"**Incorporation Date:** {data.get('incorporationDate', 'N/A')}")
            st.write(f"**Company Category:** {data.get('companyCategory', 'N/A')}")
            
            # Financial metrics
            financials = data.get('financials', {})
            
            assets = financials.get('cCalculatedTotalAssets', 0) or 0
            liabilities = financials.get('cCalculatedTotalLiabilities', 0) or 0
            equity = financials.get('cCalculatedEquity', 0) or 0
            
            # Additional financial metrics available in the new format
            current_assets = financials.get('cCalculatedTotalCurrentAssets', 0) or 0
            fixed_assets = financials.get('cCalculatedTotalFixedAssets', 0) or 0
            debt_to_equity_ratio = financials.get('cDebtToEquityRatio', None)
            debt_to_asset_ratio = financials.get('cDebtToAssetRatio', None)
            assets_growth_rate = financials.get('assetsGrowthRate', None)
            
            st.write(f"💰 Financial Data - Assets: £{assets:,.2f}, Liabilities: £{liabilities:,.2f}, Equity: £{equity:,.2f}")
            
            # Display additional financial breakdown
            if current_assets > 0 or fixed_assets > 0:
                st.write(f"📊 Asset Breakdown - Current Assets: £{current_assets:,.2f}, Fixed Assets: £{fixed_assets:,.2f}")
            
            if assets > 0 or liabilities > 0:
                
                # Create main financial overview chart
                financial_data = pd.DataFrame({
                    'Metric': ['Assets', 'Liabilities', 'Equity'],
                    'Amount': [assets, liabilities, equity]
                })
                
                fig = px.bar(financial_data, x='Metric', y='Amount', 
                           title="Financial Position (£)")
                st.plotly_chart(fig, use_container_width=True)
                
                # Create asset breakdown chart if we have the data
                if current_assets > 0 or fixed_assets > 0:
                    asset_breakdown = pd.DataFrame({
                        'Asset Type': ['Current Assets', 'Fixed Assets'],
                        'Amount': [current_assets, fixed_assets]
                    })
                    
                    fig2 = px.pie(asset_breakdown, values='Amount', names='Asset Type', 
                                title="Asset Breakdown")
                    st.plotly_chart(fig2, use_container_width=True)
                
                # Display financial ratios
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if debt_to_equity_ratio is not None:
                        st.metric("Debt-to-Equity Ratio", f"{debt_to_equity_ratio:.2f}")
                    elif equity > 0:
                        calculated_ratio = liabilities / equity
                        st.metric("Debt-to-Equity Ratio", f"{calculated_ratio:.2f}")
                    else:
                        st.metric("Debt-to-Equity Ratio", "N/A")
                
                with col2:
                    if debt_to_asset_ratio is not None:
                        st.metric("Debt-to-Asset Ratio", f"{debt_to_asset_ratio:.2f}")
                    else:
                        st.metric("Debt-to-Asset Ratio", "N/A")
                
                with col3:
                    if assets_growth_rate is not None:
                        st.metric("Assets Growth Rate", f"{assets_growth_rate:.2f}%")
                    else:
                        st.metric("Assets Growth Rate", "N/A")
                
            # Create enhanced ratio visualizations
            st.subheader("📊 Financial Health Analysis")

            # Display the key ratios in a clean metric row
            if debt_to_equity_ratio is not None or debt_to_asset_ratio is not None or assets_growth_rate is not None:
                
                # Simple, clean ratio cards
                ratio_cols = st.columns(3)
                
                with ratio_cols[0]:
                    if debt_to_equity_ratio is not None:
                        # Color code based on typical benchmarks
                        de_color = "normal"
                        if debt_to_equity_ratio > 2:
                            de_color = "inverse"
                        elif debt_to_equity_ratio > 1:
                            de_color = "off"
                        
                        st.metric(
                            "Debt-to-Equity Ratio", 
                            f"{debt_to_equity_ratio:.2f}",
                            help="Lower is generally better. >2 may indicate high leverage."
                        )
                
                with ratio_cols[1]:
                    if debt_to_asset_ratio is not None:
                        st.metric(
                            "Debt-to-Asset Ratio", 
                            f"{debt_to_asset_ratio:.1%}",
                            help="Shows what % of assets are financed by debt. Lower is generally better."
                        )
                
                with ratio_cols[2]:
                    if assets_growth_rate is not None:
                        delta_color = "normal" if assets_growth_rate > 0 else "inverse"
                        st.metric(
                            "Assets Growth Rate", 
                            f"{assets_growth_rate:.1f}%",
                            help="Year-over-year growth in total assets. Positive growth is good."
                        )
                
                st.markdown("---")
                
                # Create a simple, clear comparison chart
                available_ratios = []
                ratio_names = []
                colors = []
                
                if debt_to_equity_ratio is not None:
                    available_ratios.append(debt_to_equity_ratio)
                    ratio_names.append("D/E Ratio")
                    colors.append("#ff6b6b" if debt_to_equity_ratio > 1.5 else "#51cf66" if debt_to_equity_ratio < 0.5 else "#ffd43b")
                
                if debt_to_asset_ratio is not None:
                    available_ratios.append(debt_to_asset_ratio)
                    ratio_names.append("D/A Ratio") 
                    colors.append("#ff6b6b" if debt_to_asset_ratio > 0.6 else "#51cf66" if debt_to_asset_ratio < 0.3 else "#ffd43b")
                
                # Only show chart if we have multiple ratios
                if len(available_ratios) > 1:
                    ratio_df = pd.DataFrame({
                        'Ratio': ratio_names,
                        'Value': available_ratios
                    })
                    
                    fig_ratios = px.bar(
                        ratio_df, 
                        x='Ratio', 
                        y='Value',
                        title="Key Financial Ratios",
                        color='Value',
                        color_continuous_scale=['#51cf66', '#ffd43b', '#ff6b6b'],
                        text='Value'
                    )
                    
                    fig_ratios.update_traces(texttemplate='%{text:.2f}', textposition='outside')
                    fig_ratios.update_layout(
                        showlegend=False,
                        height=400,
                        yaxis_title="Ratio Value"
                    )
                    
                    st.plotly_chart(fig_ratios, use_container_width=True)
                
                # Growth rate gets its own simple visualization if available
                if assets_growth_rate is not None:
                    # Simple gauge-style chart using a horizontal bar
                    growth_df = pd.DataFrame({
                        'Metric': ['Assets Growth'],
                        'Growth Rate': [assets_growth_rate]
                    })
                    
                    fig_growth = px.bar(
                        growth_df,
                        x='Growth Rate',
                        y='Metric',
                        orientation='h',
                        title="Assets Growth Rate",
                        color='Growth Rate',
                        color_continuous_scale=['#ff6b6b', '#ffd43b', '#51cf66'],
                        color_continuous_midpoint=0,
                        text='Growth Rate'
                    )
                    
                    fig_growth.update_traces(texttemplate='%{text:.1f}%', textposition='auto')
                    fig_growth.update_layout(
                        showlegend=False,
                        height=200,
                        xaxis_title="Growth Rate (%)",
                        yaxis_title=""
                    )
                    
                    # Add reference lines for context
                    fig_growth.add_vline(x=0, line_dash="dash", line_color="gray", annotation_text="No Growth")
                    if assets_growth_rate != 0:
                        fig_growth.add_vline(x=5, line_dash="dot", line_color="green", annotation_text="Good Growth (5%)")
                    
                    st.plotly_chart(fig_growth, use_container_width=True)
                
                # Simple health summary
                health_indicators = []
                if debt_to_equity_ratio is not None:
                    if debt_to_equity_ratio < 0.5:
                        health_indicators.append("✅ Low debt relative to equity")
                    elif debt_to_equity_ratio < 1.5:
                        health_indicators.append("⚠️ Moderate debt levels")
                    else:
                        health_indicators.append("❌ High debt relative to equity")
                
                if debt_to_asset_ratio is not None:
                    if debt_to_asset_ratio < 0.3:
                        health_indicators.append("✅ Conservative debt financing")
                    elif debt_to_asset_ratio < 0.6:
                        health_indicators.append("⚠️ Moderate debt financing") 
                    else:
                        health_indicators.append("❌ High debt financing")
                
                if assets_growth_rate is not None:
                    if assets_growth_rate > 5:
                        health_indicators.append("✅ Strong asset growth")
                    elif assets_growth_rate > 0:
                        health_indicators.append("⚠️ Modest asset growth")
                    else:
                        health_indicators.append("❌ Declining assets")
                
                if health_indicators:
                    st.subheader("💡 Financial Health Summary")
                    for indicator in health_indicators:
                        st.write(indicator)
                
            else:
                print("DEBUG: No financial data available - all values are 0")
                st.warning("No financial data available for this company")
                
        else:
            print(f"DEBUG: API request failed with status {response.status_code}")
            print(f"DEBUG: Response content: {response.text}")
            st.error(f"Error: {response.status_code} - Check your API key and company number")
            
    except Exception as e:
        print(f"DEBUG: Exception occurred: {type(e).__name__}: {str(e)}")
        st.error(f"An error occurred: {str(e)}")

st.markdown("---")
st.caption("Powered by DataLedger API")