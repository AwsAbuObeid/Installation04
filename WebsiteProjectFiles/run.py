from flask_apscheduler import APScheduler
import csv
import numpy as np
from App.NN import Predictors
from App import app
from data.UpdateDB import UpdatePriceVolume, UpdateTech, UpdateStocks

scheduler = APScheduler()
if True:
    scheduler.add_job(func=UpdatePriceVolume, trigger='cron', id='job1', second=5)
    scheduler.add_job(func=UpdateTech, trigger='cron', id='tech1', minute=15)
    scheduler.add_job(func=UpdateTech, trigger='cron', id='tech2', minute=45)
    scheduler.add_job(func=UpdateTech, trigger='cron', id='tech3', minute=30)
    scheduler.add_job(func=UpdateTech, trigger='cron', id='tech4', minute=0)
    scheduler.add_job(func=UpdateStocks, trigger='cron', id='stoc1', minute=15)
    scheduler.add_job(func=UpdateStocks, trigger='cron', id='stoc2', minute=45)
    scheduler.add_job(func=UpdateStocks, trigger='cron', id='stoc3', minute=30)
    scheduler.add_job(func=UpdateStocks, trigger='cron', id='stoc4', minute=0)
    scheduler.add_job(func=Predictors.updateOneMinModels, trigger='cron', id='predmin', second=0)
    scheduler.add_job(func=Predictors.update15MinModels, trigger='cron', id='predfif1', minute=0)
    scheduler.add_job(func=Predictors.update15MinModels, trigger='cron', id='predfif2', minute=15)
    scheduler.add_job(func=Predictors.update15MinModels, trigger='cron', id='predfif3', minute=30)
    scheduler.add_job(func=Predictors.update15MinModels, trigger='cron', id='predfif4', minute=45)


def get_data(dr, I):
    file = open(dr)
    d = csv.reader(file)
    next(d)
    rows = []

    for row in d:
        g = []
        for index in I:
            g.append(float(row[index]))
        rows.append(g)
    data = np.array(rows)
    return data


if __name__ == "__main__":
    # db.create_all()
    scheduler.start()
    app.run(debug=True, use_reloader=False)
