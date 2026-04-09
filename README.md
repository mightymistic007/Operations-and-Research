# 🏥 NurseOptima: Algorithmic Staffing & Compliance Optimizer

**NurseOptima** is an automated healthcare management solution designed to solve complex staffing challenges using **Operations Research (OR)**. [cite_start]By integrating real-world Payroll-Based Journal (PBJ) data with mathematical optimization, the system generates staffing plans that ensure 100% regulatory compliance while minimizing unnecessary labor hours. [cite: 268, 270, 271]

## 📊 Project Overview

Healthcare facilities often struggle to balance high-quality patient care with rigid federal staffing requirements. [cite_start]This project provides a sophisticated analytical solution: [cite: 282, 283, 285]

* [cite_start]**Automated Compliance:** Mathematically ensures all facilities meet the CMS minimum Hours Per Resident Day (HPRD) for RNs, LPNs, and CNAs. [cite: 306, 420]
* [cite_start]**Operational Efficiency:** Minimizes total labor hours to reduce overutilization and operational costs. [cite: 306, 415]
* [cite_start]**Data-Driven Insights:** Replaces manual, heuristic scheduling with provably optimal staffing levels derived from real-world datasets. [cite: 289, 549]

---

## 🧪 Methodology & Mathematical Formulation

### 1. Data Cleaning & Aggregation
[cite_start]The framework processes raw CMS Payroll-Based Journal data (`Nurse_fulldata.csv`) to prepare it for the optimization engine. [cite: 346, 385]
* [cite_start]**Standardization:** Daily records for over 14,000 facilities are cleaned of missing values and zero-census days. [cite: 350, 401, 402]
* [cite_start]**Aggregation:** Data is grouped by facility ID (`PROVNUM`) to calculate total resident days and existing staffing hours for the reporting period. [cite: 72, 404]

### 2. Linear Programming Formulation
[cite_start]The core optimization model minimizes the total hours ($Z$) for each facility $f$ while satisfying federal "care floor" mandates. [cite: 292, 416]

#### **Decision Variables**
Let:
* [cite_start]$x_{RN}$ = Total optimized Registered Nurse hours [cite: 412, 413]
* [cite_start]$x_{LPN}$ = Total optimized Licensed Practical Nurse hours [cite: 412, 413]
* [cite_start]$x_{CNA}$ = Total optimized Certified Nursing Assistant hours [cite: 412, 413]

#### **Objective Function**
Minimize the Total Staffing Hours ($Z$):
[cite_start]$$Minimize: Z = x_{RN} + x_{LPN} + x_{CNA}$$ [cite: 292, 416]

#### **Constraints (CMS Regulatory Minimums)**
[cite_start]Each facility must meet the mandatory HPRD thresholds multiplied by the total resident days ($D$): [cite: 420, 424]
* [cite_start]**RN Requirement:** $x_{RN} \geq 0.75 \times D$ [cite: 298, 421]
* [cite_start]**LPN Requirement:** $x_{LPN} \geq 0.55 \times D$ [cite: 298, 422]
* [cite_start]**CNA Requirement:** $x_{CNA} \geq 2.25 \times D$ [cite: 298, 423]
* [cite_start]**Non-Negativity:** $x_{RN}, x_{LPN}, x_{CNA} \geq 0$ [cite: 412]

---

## 🛠️ Tech Stack & Implementation

* **Language:** Python 3.x
* [cite_start]**Optimization:** `PuLP` library (Linear Programming Solver) [cite: 20, 389]
* [cite_start]**Data Manipulation:** `Pandas` and `NumPy` [cite: 20, 387, 388]
* [cite_start]**Visualization:** `Matplotlib` (Bar charts) and `Pillow` (Interactive Image Viewer) [cite: 20, 390, 436]

---

## 📈 Key Results & Evaluation

* [cite_start]**Compliance Mastery:** The model successfully increased the compliance rate from an initial **4.78%** to a perfect **100%**. [cite: 170, 171, 516]
* [cite_start]**Understaffing Identification:** The analysis revealed a massive deficit in current staffing, requiring a net increase of **~26.2 million hours** to meet legal safety standards. [cite: 518]
* [cite_start]**Resource Optimization:** While adding hours where needed, the model also identified thousands of "Overstaffed" instances, allowing for potential reallocation of resources. [cite: 537, 546]

---

## 📂 Project Structure

```text
Nurse-Staffing-Optimization
├── OR_1.IPYNB          # Jupyter Notebook: Data Cleaning & PuLP Solver Logic
├── OR_Final_Report.pdf  # Final academic report (Methodology & Results)
├── OR_FINAL_REVIEW.pptx # Stakeholder presentation and visualization
├── OR.docx              # Detailed technical documentation and literature review
├── final_results.csv    # Final optimized data used for dashboard/reporting
└── README.md            # Project documentation (This file)
