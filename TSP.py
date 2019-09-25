from GA import GA
from TravelSalesPerson import TravelSalesPerson
from Logger import Logger
import numpy as np
log = Logger('test.log', level='info')

import datetime

starttime = datetime.datetime.now()

CROSS_RATE = 0.1        # 交叉概率
MUTATE_RATE = 0.02      # 突变概率
POP_SIZE = 10           # 种群大小
N_GENERATIONS = 20000     # 迭代轮数
DATA_SET = 'KROC100'      # 从10个数据集中选择使用其中一个，在这里写数据集的名字即可


env = TravelSalesPerson(DATA_SET)
N_CITIES = env.N_CITIES
ga = GA(DNA_size=N_CITIES, cross_rate=CROSS_RATE, mutation_rate=MUTATE_RATE, pop_size=POP_SIZE)
log.logger.info('种群产生完成，种群大小为{}，每个个体的DNA长度为{}'.format(ga.pop_size, ga.DNA_size))

for generation in range(N_GENERATIONS):
    lx, ly = ga.translateDNA(ga.pop, env.city_position)
    fitness, total_distance = ga.get_fitness(lx, ly)
    distance_list = total_distance.tolist()
    ga.evolve_elitism(fitness)
    if generation % 100 == 99:
        print('正在进行第{}轮迭代'.format(str(generation + 1)))
        log.log_write('Generation {}, the best fitness in the current population is {}'.format(str(generation + 1), str(np.max(fitness))))
    if generation == 4999 or generation == 9999 or generation == 19999:
        best_distance = np.min(total_distance)
        best_route = ga.pop[np.argmin(total_distance)]
        out_best_route = '-'.join(map(str, best_route.tolist()))    # 加上分隔符输出
        print('当前种群中表现最佳的总路程{}'.format(str(best_distance)))
        print('当前种群中表现最佳的路径{}'.format(out_best_route))
    if generation == 9999:
        endtime = datetime.datetime.now()
    if (datetime.datetime.now() - starttime).seconds > 8 * 60 * 60:
        best_distance = np.min(total_distance)
        best_route = ga.pop[np.argmin(total_distance)]
        out_best_route = '-'.join(map(str, best_route.tolist()))    # 加上分隔符输出
        print('程序进行了8小时，停止迭代')
        print('当前代数{}，最佳总路程{}，最佳适应度{}'.format(str(generation), str(best_distance), str(np.max(fitness))))
        print('当前最优路径{}'.format(out_best_route))
        exit()

print('10000代程序运行时间：{}秒'.format((endtime - starttime).seconds))