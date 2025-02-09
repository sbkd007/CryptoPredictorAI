import streamlit as st
import cv2
import numpy as np
from PIL import Image
import plotly.graph_objects as go
from utils.image_processor import process_image
from utils.trend_analyzer import analyze_trends

def main():
    st.set_page_config(
        page_title="Crypto Trend Analyzer",
        page_icon="📈",
        layout="wide"
    )

    st.title("Cryptocurrency Trend Analyzer 📈")
    st.markdown("""
    Upload a cryptocurrency graph image to analyze trends across different timeframes.
    The analyzer will provide insights and trading recommendations based on the pattern analysis.
    """)

    uploaded_file = st.file_uploader("Choose a graph image", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        try:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            col1, col2 = st.columns(2)
            with col1:
                st.image(image, caption='Uploaded Graph', use_column_width=True)

            # Process image
            with st.spinner('Processing image...'):
                # Convert PIL Image to numpy array
                image_array = np.array(image)
                processed_image = process_image(image_array)
                
                # Analyze trends
                trends = analyze_trends(processed_image)

            # Display results
            with col2:
                st.subheader("Analysis Results")
                
                # Create timeframe analysis table
                timeframes = ['5 minutes', '10 minutes', '20 minutes', '40 minutes', '1 hour', '1 day']
                
                # Create plotly figure for trends
                fig = go.Figure()
                
                for idx, timeframe in enumerate(timeframes):
                    trend = trends[timeframe]
                    
                    # Add trend line to plot
                    fig.add_trace(go.Scatter(
                        x=[idx, idx + 1],
                        y=[0, trend['slope']],
                        name=timeframe,
                        mode='lines',
                        line=dict(
                            color='green' if trend['direction'] == 'up' else 'red',
                            width=2
                        )
                    ))
                
                fig.update_layout(
                    title='Trend Analysis by Timeframe',
                    xaxis_title='Timeframe',
                    yaxis_title='Trend Strength',
                    showlegend=True,
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)

                # Display recommendations
                st.subheader("Trading Recommendations")
                for timeframe, trend in trends.items():
                    confidence = trend['confidence']
                    direction = trend['direction']
                    recommendation = "BUY" if direction == "up" else "SELL"
                    
                    color = "green" if direction == "up" else "red"
                    st.markdown(f"""
                    <div style='padding: 10px; border-radius: 5px; background-color: rgba({color}, 0.1)'>
                        <strong>{timeframe}:</strong> {recommendation} 
                        (Confidence: {confidence:.1f}%)
                        <br>
                        Trend: {direction.upper()}
                    </div>
                    """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
            st.info("Please ensure you upload a clear graph image for accurate analysis.")

if __name__ == "__main__":
    main()
