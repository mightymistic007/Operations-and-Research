# 🏛️ CivicSpend Optimizer: Municipal Budget Allocation Framework

The **CivicSpend Optimizer** is a data-driven framework designed to enhance the efficiency of municipal budget allocations by combining unsupervised machine learning with mathematical optimization. 

## 📊 Project Overview

Urban centers often struggle with rigid, historical budgeting processes that fail to reflect current socio-economic needs. This project provides a two-stage analytical solution:

* **Stage 1 (Pattern Discovery):** Uses **K-Means Clustering** to categorize municipal departments based on spending trends and population impact.
* **Stage 2 (Optimization):** Uses **Linear Programming (Simplex Method)** via **Google OR-Tools** to determine the exact dollar amount each department should receive to maximize overall city utility.

---

## 🧪 Detailed Methodology & Mathematical Formulation

### 1. Data Preprocessing & Feature Engineering
The framework utilizes a dataset representing typical municipal sectors: Healthcare, Education, Infrastructure, Public Safety, and Welfare.
* **Feature Scaling:** Data was normalized using `StandardScaler` to ensure the clustering algorithm wasn't biased by the magnitude of budget figures.
* **Utility Metric:** A "Utility Score" was derived for each sector based on historical ROI and population reach.

### 2. Unsupervised Clustering (K-Means)
K-Means clustering is applied to identify "High-Need" vs. "High-Efficiency" sectors.
* **Elbow Method:** Used to determine the optimal number of clusters ($k=3$), balancing intra-cluster variance.
* **Clustering Objective:**
    $$\text{Minimize } J = \sum_{i=1}^{k} \sum_{x \in C_i} ||x - \mu_i||^2$$
    Where $\mu_i$ is the centroid of cluster $C_i$.

### 3. Linear Programming Formulation
The core optimization model maximizes the city’s benefit within a fixed budget $B$.

#### **Decision Variables**
Let $x_i$ be the budget allocated to sector $i$.

#### **Objective Function**
Maximize the Total Utility ($Z$):
$$Z = \sum_{i=1}^{n} U_i \cdot x_i$$
Where $U_i$ is the utility coefficient for sector $i$.

#### **Constraints**
* **Total Budget Constraint:** The sum of all allocations cannot exceed available municipal funds ($B$):
    $$\sum_{i=1}^{n} x_i \leq B$$
* **Minimum Operational Funding:** Each sector must receive at least a baseline amount to function:
    $$x_i \geq \text{Min}_i$$
* **Capacity Constraint:** No sector can receive more than its maximum administrative capacity:
    $$x_i \leq \text{Max}_i$$
   .

---

## 🛠️ Tech Stack & Implementation Details

* **Language:** Python 3.10+.
* **Optimization Engine:** `Google OR-Tools` (Linear Solver).
* **Data Science:** `Scikit-learn` for K-Means and `Pandas` for data manipulation.
* **Interface:** `Streamlit` was used to build an interactive dashboard where city officials can adjust constraints in real-time.

---

## 📈 Key Results & Evaluation

* **Efficiency Gain:** The optimized model showed a significant increase in total utility compared to equal-weight or historical allocation methods.
* **Sensitivity Analysis:** The model was tested against varying budget cuts, demonstrating that the Linear Programming model protects "Critical Need" sectors (identified in Stage 1) more effectively than traditional methods.

---

## 📂 Project Structure

```text
CivicSpend-Optimizer
├── OR_1.IPYNB          # Development Notebook: Clustering & Solver Logic
├── OR_Final_Report.pdf # Comprehensive research and results analysis
├── OR_FINAL_REVIEW.pptx# Presentation for municipal stakeholders
├── OR.docx             # Project documentation and literature survey
└── README.md           # Documentation (This file)
