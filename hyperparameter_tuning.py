from genetic_optimizer import GeneticOptimizer
import numpy as np


def generate_hyperparameters(k):
    """
    generate k sets of hyperparameters randomly : (mutate_prob, elite, alpha, beta)

    Args:
        k: number of sets

    Returns:
        list of settings, where each setting is a set of hyperparameters
    """
    settings = []
    for i in range(k):
        setting = [np.random.rand(), np.random.randint(3, 20), np.random.rand(), np.random.rand()]
        settings.append(setting)
    return settings


def random_search(k):
    """
    fix experiment setting: run genetic optimizer with student_count=50 and faculty_count=15 for 100 epoches
    explore the best set hyperparameters on this experiment

    Args:
        k: number of sets of hyperparameters to search

    Returns:
        the best set of hyperparameters (with lowest loss)
    """
    settings = generate_hyperparameters(k)
    lowest_loss_list = []
    for setting in settings:
        temp_mutate_prob, temp_elite, temp_alpha, temp_beta = setting
        optimizer = GeneticOptimizer(population_size=100, student_count=50, faculty_count=15, epoch=100,
                                     mutate_prob=temp_mutate_prob, elite=temp_elite, alpha=temp_alpha, beta=temp_beta,
                                     hyperparam_search=True)

        optimizer.evolution()
        lowest_loss_list.append(optimizer.lowest_loss)

    idx_list = list(np.array(lowest_loss_list).argsort())
    res_idx = idx_list[0]
    print(f"best hyperparameter setting is the {res_idx}th one. "
          f"\n       It has lowest loss = {lowest_loss_list[res_idx]} \n\n")
    return settings[res_idx]


'''
output log

current setting : mutate_prob = 0.7830585862109902, elite = 8, alpha = 0.10548112061021409, beta = 0.7255343917730384.  
         Lowest loss = 234.00582490123753 

current setting : mutate_prob = 0.927900001228505, elite = 14, alpha = 0.6432144617787491, beta = 0.12138613933841225.  
         Lowest loss = 263.98030977789415 

current setting : mutate_prob = 0.5685238410898966, elite = 15, alpha = 0.5291291187478512, beta = 0.06226794121747514.  
         Lowest loss = 233.97297736690294 

current setting : mutate_prob = 0.9022363540546243, elite = 11, alpha = 0.29985117379444026, beta = 0.7734301754342513.  
         Lowest loss = 269.00043440878096 

current setting : mutate_prob = 0.7617320927074978, elite = 5, alpha = 0.7594422472157214, beta = 0.8018500167526038.  
         Lowest loss = 282.0063130456911 

current setting : mutate_prob = 0.4118412145521758, elite = 4, alpha = 0.7441564312802005, beta = 0.06845997384951463.  
         Lowest loss = 227.9732584732175 

current setting : mutate_prob = 0.7997860572848272, elite = 3, alpha = 0.14200191367933235, beta = 0.8696029348510791.  
         Lowest loss = 244.9897356839867 

current setting : mutate_prob = 0.7130661010688488, elite = 15, alpha = 0.46746241851069814, beta = 0.04137501619398265.  
         Lowest loss = 236.9687207315526 

current setting : mutate_prob = 0.11110769007438848, elite = 7, alpha = 0.15024974991644768, beta = 0.8594668522649078.  
         Lowest loss = 267.01387341466574 

current setting : mutate_prob = 0.8443309484569906, elite = 12, alpha = 0.9079895478168457, beta = 0.7010758064241582.  
         Lowest loss = 283.0442773518015 

current setting : mutate_prob = 0.6889950120136835, elite = 7, alpha = 0.6967474234830262, beta = 0.3917497120925846.  
         Lowest loss = 276.0149547728049 

current setting : mutate_prob = 0.4550997112605075, elite = 6, alpha = 0.9940021147084548, beta = 0.6812850595809498.  
         Lowest loss = 283.0172928768016 

current setting : mutate_prob = 0.4932564017118609, elite = 19, alpha = 0.058463723737744444, beta = 0.9718008608013436.  
         Lowest loss = 237.9769058933351 

current setting : mutate_prob = 0.7688077356354149, elite = 5, alpha = 0.41608614624152185, beta = 0.39736430301943604.  
         Lowest loss = 271.017085838661 

current setting : mutate_prob = 0.028584458443517646, elite = 3, alpha = 0.03151321734547596, beta = 0.7037448477595643.  
         Lowest loss = 268.98030977789426 

current setting : mutate_prob = 0.7987995906676748, elite = 15, alpha = 0.14401302236582725, beta = 0.7782955801933258.  
         Lowest loss = 246.98509105511772 

current setting : mutate_prob = 0.09086815571688867, elite = 10, alpha = 0.2069504307838953, beta = 0.9565537795147788.  
         Lowest loss = 273.014345557572 

current setting : mutate_prob = 0.10082409500043188, elite = 9, alpha = 0.2915201458430329, beta = 0.9118749974512508.  
         Lowest loss = 281.99448046379075 

current setting : mutate_prob = 0.009763908205011718, elite = 16, alpha = 0.11898104015435773, beta = 0.7565534159385289.  
         Lowest loss = 280.0231399345875 

current setting : mutate_prob = 0.6679869630806617, elite = 11, alpha = 0.1727374912442804, beta = 0.5784665370510903.  
         Lowest loss = 251.01680473234777 

current setting : mutate_prob = 0.09820213173015124, elite = 6, alpha = 0.3645158550148814, beta = 0.5362227196003507.  
         Lowest loss = 270.00549679231784 

current setting : mutate_prob = 0.5753519108447077, elite = 19, alpha = 0.9984108639122673, beta = 0.8123172960820205.  
         Lowest loss = 288.02279025646055 

current setting : mutate_prob = 0.5657953823491493, elite = 16, alpha = 0.44908815480205455, beta = 0.019510656010950034.  
         Lowest loss = 222.9769058933351 

current setting : mutate_prob = 0.2741742519816275, elite = 13, alpha = 0.43790195202072846, beta = 0.5477180028566037.  
         Lowest loss = 284.0141169502229 

current setting : mutate_prob = 0.21086310539402764, elite = 8, alpha = 0.7683905281463057, beta = 0.7035069025575326.  
         Lowest loss = 287.0054967923179 

current setting : mutate_prob = 0.5585539152826466, elite = 17, alpha = 0.41556908342610943, beta = 0.44531356092104546.  
         Lowest loss = 275.96961105309856 

current setting : mutate_prob = 0.8521192887448478, elite = 8, alpha = 0.9163231113748435, beta = 0.5223937882850253.  
         Lowest loss = 274.0010436240141 

current setting : mutate_prob = 0.8938303458295986, elite = 12, alpha = 0.22431270098654266, beta = 0.14859428212255488.  
         Lowest loss = 259.0290686182846 

current setting : mutate_prob = 0.02961204369424586, elite = 14, alpha = 0.8427923903288946, beta = 0.8211539420890231.  
         Lowest loss = 279.9802252045329 

current setting : mutate_prob = 0.6440868991938821, elite = 11, alpha = 0.7607616149386083, beta = 0.3344505813389165.  
         Lowest loss = 269.0068221099875 

best hyperparameter setting is the 22th one. 
       It has lowest loss = 222.9769058933351 


mutate_prob = 0.5657953823491493, elite = 16, alpha = 0.44908815480205455, beta = 0.019510656010950034
'''
if __name__ == "__main__":
    best_setting = random_search(30)
    mutate_prob, elite, alpha, beta = best_setting
    print(f"mutate_prob = {mutate_prob}, elite = {elite}, alpha = {alpha}, beta = {beta}")
