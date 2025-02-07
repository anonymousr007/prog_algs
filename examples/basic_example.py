# Copyright © 2021 United States Government as represented by the Administrator of the National Aeronautics and Space Administration. All Rights Reserved.

"""
This example performs a state estimation and prediction with uncertainty given a Prognostics Model.
 
Method: An instance of the BatteryCircuit model in prog_models is created, and the prediction process is achieved in three steps:
    1) State estimation of the current state is performed using a chosen state_estimator, and samples are drawn from this estimate
    2) Prediction of future states (with uncertainty) and the times at which the event threshold will be reached
    3) Metrics tools are used to further investigate the results of prediction
Results: 
    i) Predicted future values (inputs, states, outputs, event_states) with uncertainty from prediction
    ii) Time event is predicted to occur (with uncertainty)
    iii) Various prediction metrics
    iv) Figures illustrating results
"""

from prog_models.models import BatteryCircuit as Battery
# VVV Uncomment this to use Electro Chemistry Model VVV
# from prog_models.models import BatteryElectroChem as Battery

from prog_algs import *

def run_example():
    # Step 1: Setup model & future loading
    def future_loading(t, x = None):
        # Variable (piece-wise) future loading scheme 
        if (t < 600):
            i = 2
        elif (t < 900):
            i = 1
        elif (t < 1800):
            i = 4
        elif (t < 3000):
            i = 2
        else:
            i = 3
        return {'i': i}
    batt = Battery()
    initial_state = batt.parameters['x0']

    # Step 2: Demonstrating state estimator
    print("\nPerforming State Estimation Step")

    # Step 2a: Setup
    filt = state_estimators.ParticleFilter(batt, initial_state)
    # VVV Uncomment this to use UKF State Estimator VVV
    # filt = state_estimators.UnscentedKalmanFilter(batt, initial_state)

    # Step 2b: Print & Plot Prior State
    print("Prior State:", filt.x.mean)
    print('\tSOC: ', batt.event_state(filt.x.mean)['EOD'])
    fig = filt.x.plot_scatter(label='prior')

    # Step 2c: Perform state estimation step
    example_measurements = {'t': 32.2, 'v': 3.915}
    t = 0.1
    filt.estimate(t, future_loading(t), example_measurements)

    # Step 2d: Print & Plot Resulting Posterior State
    print("\nPosterior State:", filt.x.mean)
    print('\tSOC: ', batt.event_state(filt.x.mean)['EOD'])
    filt.x.plot_scatter(fig=fig, label='posterior')  # Add posterior state to figure from prior state

    # Note: in a prognostic application the above state estimation step would be repeated each time
    #   there is new data. Here we're doing one step to demonstrate how the state estimator is used

    # Step 3: Demonstrating Predictor
    print("\n\n\nPerforming Prediction Step")

    # Step 3a: Setup Predictor
    mc = predictors.MonteCarlo(batt)

    # Step 3b: Perform a prediction
    NUM_SAMPLES = 20
    # Sample from the latest state in the state estimator
    # Note: This is only required for sample-based prediction algorithms
    samples = filt.x.sample(NUM_SAMPLES)  
    STEP_SIZE = 0.1
    (times, inputs, states, outputs, event_states, toe) = mc.predict(samples, future_loading, dt=STEP_SIZE)
    print('ToE', toe.mean)

    # Step 3c: Analyze the results

    # Note: The results of a sample-based prediction can be accessed by sample, e.g.,
    states_sample_1 = states[1]
    # now states_sample_1[n] corresponds to times[n] for the first sample

    # You can also access a state distribution at a specific time using the .snapshot function
    states_time_1 = states.snapshot(1)
    # now you have all the samples corresponding to times[1]
    
    # You can also use the metrics package to generate some useful metrics on the result of a prediction
    print("\nEOD Prediction Metrics")
    toe = toe.key('EOD') # Calculate metrics for event EOL

    from prog_algs.metrics import samples as metrics 
    print('\tPercentage between 3005.2 and 3005.6: ', metrics.percentage_in_bounds(toe, [3005.2, 3005.6])*100.0, '%')
    print('\tAssuming ground truth 3002.25: ', metrics.toe_metrics(toe, 3005.25))
    print('\tP(Success) if mission ends at 3002.25: ', metrics.prob_success(toe, 3005.25))

    # Plot state transition 
    # Here we will plot the states at t0, 25% to ToE, 50% to ToE, 75% to ToE, and ToE
    fig = states.snapshot(0).plot_scatter(label = "t={} s".format(int(times[0])))  # 0
    quarter_index = int(len(times)/4)
    states.snapshot(quarter_index).plot_scatter(fig = fig, label = "t={} s".format(int(times[quarter_index])))  # 25%
    states.snapshot(quarter_index*2).plot_scatter(fig = fig, label = "t={} s".format(int(times[quarter_index*2])))  # 50%
    states.snapshot(quarter_index*3).plot_scatter(fig = fig, label = "t={} s".format(int(times[quarter_index*3])))  # 75%
    states.snapshot(-1).plot_scatter(fig = fig, label = "t={} s".format(int(times[-1])))  # 100%

    # Step 4: Show all plots
    import matplotlib.pyplot as plt  # For plotting
    plt.show()

# This allows the module to be executed directly 
if __name__ == '__main__':
    run_example()
