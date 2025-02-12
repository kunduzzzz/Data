{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 27,
   "id": "c24b169e-b75a-4592-b026-019486bb73b9",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "DeltaGenerator()"
      ]
     },
     "execution_count": 27,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import streamlit as st  # 导入 Streamlit 库，用于创建 Web 应用\n",
    "import pandas as pd  # 导入 Pandas 库，用于数据处理\n",
    "import pickle  # 导入 pickle 库，用于加载已训练的模型\n",
    "import os  # 导入 os 库，用于处理文件路径\n",
    "import shap  # 导入 SHAP 库，用于解释模型\n",
    "\n",
    "# 获取当前文件的目录\n",
    "model_path = \"C:\\\\Users\\\\kunduz\\\\xgboost_model.pkl\"\n",
    "with open(model_path, 'rb') as file:\n",
    "    model = pickle.load(file)\n",
    "# 侧边栏输入\n",
    "with st.sidebar:\n",
    "    st.header(\"患者参数输入\")\n",
    "    st.subheader(\"卵巢储备指标\")\n",
    "    amh = st.slider(\"AMH (ng/mL)\", min_value=0.0, max_value=10.0, value=3.0, step=0.1)\n",
    "    afc = st.slider(\"AFC (个)\", min_value=0, max_value=40, value=15, step=1)\n",
    "    fsh = st.slider(\"基础FSH (IU/L)\", min_value=1.0, max_value=20.0, value=8.0, step=0.1)\n",
    "    \n",
    "    st.subheader(\"基础特征\")\n",
    "    age = st.slider(\"年龄 (years old)\", min_value=18, max_value=50, value=30)\n",
    "\n",
    "# 检查输入值是否为有效的数字（即确保没有 NaN）\n",
    "if amh is None or afc is None or fsh is None or age is None:\n",
    "    st.error(\"输入值不能为空，请重新输入\")\n",
    "else:\n",
    "    # 创建输入数据框\n",
    "    input_data = pd.DataFrame({\n",
    "        'AMH': [amh],\n",
    "        'AFC': [afc],\n",
    "        'FSH': [fsh],\n",
    "        'age': [age],\n",
    "    })\n",
    "\n",
    "    # 预测与解释\n",
    "    col1, col2 = st.columns([1, 2])\n",
    "\n",
    "    with col1:\n",
    "        if st.button(\"开始风险评估\"):\n",
    "            # 概率预测\n",
    "            prob = model.predict_proba(input_data)[0][1]\n",
    "            risk_level = \"高风险\" if prob >= 0.6 else \"中风险\" if prob >= 0.3 else \"低风险\"\n",
    "            \n",
    "            # 临床解读\n",
    "            st.subheader(\"评估结果\")\n",
    "            \n",
    "            # 使用 st.metric 显示预测概率和风险等级\n",
    "            st.metric(label=\"预测概率\", value=f\"{prob:.2%}\")\n",
    "            st.metric(label=\"风险等级\", value=risk_level)\n",
    "            \n",
    "            st.markdown(f\"\"\"\n",
    "            **临床建议**:\n",
    "            - {\">5% Gn剂量减少\" if risk_level == \"高风险\" else \"常规剂量\"}\n",
    "            - {\"建议使用拮抗剂方案\" if risk_level == \"高风险\" else \"可考虑长方案\"}\n",
    "            - {\"建议冷冻全胚\" if risk_level == \"高风险\" else \"可考虑鲜胚移植\"}\n",
    "            \"\"\")\n",
    "\n",
    "    with col2:\n",
    "        if 'prob' in locals():\n",
    "            st.subheader(\"风险因素解析\")\n",
    "            \n",
    "            # SHAP解释\n",
    "            explainer = shap.TreeExplainer(model)\n",
    "            shap_values = explainer.shap_values(input_data)\n",
    "            \n",
    "            # 可视化设置\n",
    "            st.set_option('deprecation.showPyplotGlobalUse', False)  # 隐藏警告\n",
    "            shap.summary_plot(shap_values, input_data, plot_type=\"bar\", show=False)\n",
    "            st.pyplot()\n",
    "\n",
    "            # 特征解释文本\n",
    "            st.markdown(\"\"\"\n",
    "            **特征说明**:\n",
    "            - 正值增加风险，负值降低风险\n",
    "            - AMH/AFC是主要预测因子，BMI呈U型影响\n",
    "            \"\"\")\n",
    "\n",
    "# 注意事项\n",
    "st.markdown(\"---\")\n",
    "st.warning(\"\"\"\n",
    "**使用限制**:\n",
    "1. 适用于未接受过卵巢手术的患者\n",
    "2. 多囊卵巢患者需结合超声评估\n",
    "3. 最终决策需结合临床判断\n",
    "\"\"\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
