## Enhanced SEIRS+ 
# E-SEIRS+: A Generalized Infectious Disease Model


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

### Model Calibration
Initial run with best parameter estimates: for the day prior to the simulation run (t0 - 1 day), 30 November 2020, we make point estimates of input parameters and run the model. Then, using historically reported actual data, we inspect our results and compute the mean squared error (MSE) of the generated time series to measure the model’s predictive power.
Parameter tuning and optimization: the parameters are tuned by exploring the reasonable ranges of the key input parameters identified from the initial run. To do this, we developed a design of experiments that generates 17 model instantiations with space-filling estimates of the key parameters. By inspecting the results and calculating the MSE of each of the 17 model runs, the parameters are then further refined by selecting the parameter values that best fit the historical data for t0 (December, 2020).


### Model Testing 
Update initial conditions for t1: update initial conditions for the test run. In this case, the number of cases and fatalities reported on 31 December, 2020 so those numbers are provided to the model 
Run model for t1: with the updated initial conditions and tuned parameters from the model calibration step, we then run the model for January, 2021.
Model assessment: model predictions for January are compared to the actual data for January to measure the model’s out of sample, post calibration performance.
Results
Below, Figures 1 and 2 are time series plots of COVID cases and fatalities, respectively, for December, 2020 based on information known on 30 November. Figures 3 and 4 are predictions for January 2021 based on input parameters tuned from December and actual cases and fatalities on 31 December 2020.


Figure 1: Backcast COVID Cases for December 2020. MSEcases = 76.2 cases


Figure 2: Backcast COVID Fatalities for December 2020. MSEfatalities = 7.5 fatalities


Figure 3: Forecast COVID Cases for January 2021 (MSEcases = 146.2 cases)


Figure 4: Forecast COVID Fatalities for January 2021. MSEfatalities = 5.8 fatalities.




### Discussion
The December, 2020 simulation run is our training “set”. Balanced against actual results and after parameter tuning, E-SEIRS+ produced reasonable results when applied to the test set simulation for January 2021 (Figures 3 and 4).  Some parameters were easily and confidently estimated, while others required estimation based on several experimental model runs and reasonable known ranges.  Below is a discussion of some of the more influential parameters:

Number of cases, initI: Common metric and widely available, but subject to reporting errors and reporting frequency (i.e. daily, weekly, etc) that may bias the actual results.

Number of fatalities, initF: Common metric and widely available, but as above, counting guidelines vary and reporting frequency may affect the shape of the time series data thereby skewing the MSE.

Reproduction Number, Ro: Common metric and widely available, but with a significant degree of uncertainty and model sensitivity. Through experimentation with E-SEIRS+, there is an inflection point between 1.4 to 1.5 where Ro=1.5 provides a reasonable estimate of total number of cases, but Ro= 1.4 leads to overly optimistic results where predicted cases quickly and significantly diverge from actual cases. This sensitivity highlights the need for an analyst to explore historical model runs prior to making a true prediction.

Fatality rate, mu_o: Less straightforward to find and may require transformation. For Oregon we converted what we could find (5-5.9 deaths per 1 million people) to a daily death rate. In general, the model appears to be stable and reasonable for a wide range of fatality rates.  For the short simulations of one month, despite our parameter tuning for December, it did not appear that we over-fit the training set and the January test set results were acceptable.













### Citation
1. SEIRS Model Description at https://github.com/ryansmcgee/seirsplus/wiki/SEIRS-Model-Description under the MIT License.


### Appendix A
| Parameter | Parameter Description                                    | Test Values | In LocaleDB? | Parameter Type1 | Source |
| --------- | -------------------------------------------------------- | ----------- | ------------ | --------------- | ------ |
| sigma     | Rate of progression: reciprocal of incubation period     | 5.2\-1      | No           | Disease         | 1      |
| gamma     | Rate of recovery: inverse of infectious period           | 0.06        | No           | Disease         | 2      |
| R0        | Contact infection                                        | 1.5         | No           | Geo             | 3      |
| xi        | rate of re-susceptibility                                | 0.0001      | No           | Disease         | 4      |
| mu\_I     | rate of infection-related mortality                      | 0.000150    | No           | Disease         | 5      |
| mu\_0     | rate of baseline mortality                               | 0.0002      | No           | Geo             | 6      |
| nu        | rate of baseline birth                                   | 0.099       | No           | Geo             | 7      |
| theta     | rate of testing of individuals                           | 0.01        | No           | Geo             | 8      |
| psi\_E    | probability of positive tests for exposed individuals    | 0.99        | No           | Geo             | 9      |
| psi\_I    | probability of positive tests for infectious individuals | 0.99        | No           | Geo             | 9      |
| initN     | initial total number of individuals                      | 4,283,747   | Yes          | Geo             | 10     |

       
1. Parameter Type: 
  - Disease:  the input parameter value is dependent on the disease and agnostic to geospatial and temporal consideration.
  - Geo: the input parameter value is dependent not only on the disease, but also the location and time of the model run. 

2. Oregon does not track number of recovered individuals: https://www.oregon.gov/oha/ERD/Pages/OHA-changes-recovered-cases-reporting.aspx


### Sources:
1. https://www.cdc.gov/coronavirus/2019-ncov/symptoms-testing/symptoms.htmlCDC_AA_refVal=https%3A%2F%2Fwww.cdc.gov%2Fcoronavirus%2F2019-ncov%2Fabout%2Fsymptoms.html

2. https://www.medscape.com/answers/2500114-197447/what-is-the-clinical-progression-of-coronavirus-disease-2019-covid-19#:~:text=A%20retrospective%2C%20single%2Dcenter%20study,%25)%20of%20patients%20developed%20fever.

3. https://covidactnow.org/us/oregon-or/?s=1578518

4. https://www.nature.com/articles/d41586-021-00071-6

5. http://www.healthdata.org/sites/default/files/files/Projects/COVID/briefing_Oregon_20201223.pdf

6. https://www.oregon.gov/oha/PH/BIRTHDEATHCERTIFICATES/VITALSTATISTICS/DEATH/Documents/dmon19.pdf

7. https://www.oregon.gov/oha/PH/BIRTHDEATHCERTIFICATES/VITALSTATISTICS/ANNUALREPORTS/Pages/index.aspx

8. https://www.oregon.gov/oha/covid19/Documents/DataReports/Oregon-COVID-19-Update-02-05-2021-FINAL.pdf

9. https://covidactnow.org/us/oregon-or/?s=1559499

10. https://covidtracking.com/data/state/oregon/cases




