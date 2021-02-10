# Enhanced SEIRS+ 
## E-SEIRS+: A Generalized Infectious Disease Model

## Contents
1. [Objective](#objective)
2. [Background](#background)
3. [Further Reading](#further-reading)
4. [Quick Start](#quick-start)
5. [Output Description](#output-description)
6. [License](#license)
7. [Appendix](#appendix)


### Objective
Re-engineer an existing open source epidemiological model to simplify input parameter value selection for general modelers while maintaining model efficacy. Automate verification, validation, uncertainty quantification, and sensitivity analysis of the model by leveraging LocaleDB, a database of global locales to support modeling and simulation in epidemiology with the current focus on the COVID 19 pandemic.


### Background
At the December 2020 World Modeler Exercise our Ethiopian partners expressed a need for a COVID prediction model in CauseMos. This effort aims to meet that need by enhancing the SEIRS+ model with a method to predict model parameters with readily available data. Additionally, this effort aims to assess the extent to which the ASKE structured data project, LocaleDB, may be used to automate model assessment.

This open source implementation of SEIR is a standard compartmental model in which the population is divided into susceptible (S), exposed (E), infectious (I), recovered (R) and fatality (F) individuals. See model description for more detail.
  

The rates of transition between the states are given by the parameters:
σ: rate of progression (inverse of incubation period)
γ: rate of recovery (inverse of infectious period)
ξ: rate of re-susceptibility (inverse of temporary immunity period; 0 if permanent immunity)
μI: rate of mortality from the disease (deaths per infectious individual per time)
Model Assessment
SEIRS+ requires twenty two input parameters (Appendix A). With such a high number of parameters, accurately populating each, even for backcasting, is cumbersome and error-prone. To overcome this shortfall, we developed a two-stage model calibration method to select appropriate parameters for model assessment. For this assessment, we arbitrarily selected the State of Oregon, USA.

This method includes running the model over historical data t0 (December, 2020) and minimizing the mean-squared error of predicted cases and deaths versus actual cases and deaths by varying parameters within a given generally accepted range. Then, with the best parameter values from the first step, the model is used to predict cases and deaths in an additional, historic time interval t1 (January, 2021). Specifically, below is the backcasting process we implemented:

### Further Reading:
- For further discussion of this implementation, see the google doc at [HERE](https://docs.google.com/document/d/1fgOCZBjfO7Yw3_f-yHGdOtLBg1hmeMWYVFY_zqTYwW4/edit?usp=sharing)
- The original SEIRS+ repository is [HERE](https://github.com/ryansmcgee/seirsplus)

### Quick Start

1. Clone repo

2. SPin up localedb...or add own and format

3. Go to procedure of choice

4. Update creds

5. Update params

6. run it

### Output Description
1. descr 
2. Plot it if desired

### License
1. SEIRS Model MIT License information is [HERE](https://github.com/ryansmcgee/seirsplus/blob/master/LICENSE).


### Appendix
| Parameter | Parameter Description                                    |
| --------- | -------------------------------------------------------- |
| sigma     | Rate of progression: reciprocal of incubation period     |
| gamma     | Rate of recovery: inverse of infectious period           |
| R0        | Contact infection                                        |
| xi        | rate of re-susceptibility                                |
| mu\_I     | rate of infection-related mortality                      |
| mu\_0     | rate of baseline mortality                               |
| nu        | rate of baseline birth                                   |
| theta     | rate of testing of individuals                           |
| psi\_E    | probability of positive tests for exposed individuals    |
| psi\_I    | probability of positive tests for infectious individuals |
| initN     | initial total number of individuals                      |







