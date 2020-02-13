# функция, для подсчета баллов в боте.
from datetime import datetime, date, time
def day_t(): # передает актуальный день
    today = datetime.today()
    days=today.day
    #print (days)
    return days
class peopleCounter(): #каждый участник, объект этого класса
    def __init__(self, ball,balls,event):
        self.ball = ball
        self.event = event
        self.balls = balls
    def add_Ball(self,event,ball): #получает баллы из базы, по умолчанию ноль и отправляет, каждого участника по отдельности
        if (event==1):#сданный вовремя
            ball+=1
        elif(event==2):#не сданный
            ball-=0,5 # надо тестить
        elif(event==3):#сданный долг
            ball+=0.5
        return ball

    def Balls(self, ball):# общие баллы участников
        balls=0
        balls=balls+ball
        return balls

class teamCounter():# каждая команда является объектом этого класса
    def __index__(self, balls, days, number_people,total_day,team_ball,summ_team_balls):
        self.balls = balls
        self.days=days
        self.number_people=number_people
        self.total_day = total_day
        self.team_ball=team_ball
        self.summ_team_balls=summ_team_balls

    def counter(self,balls,days,number_people):# количество людей брать из базы(это число непостоянное)
        day_balls = balls/(days*number_people) # balls тоже будут браться из базы, пока не знаю,Как их туда добавить
        total_day = day_balls*100
        return total_day

    def sumar_day_balls(self,total_day):
        if (total_day == 100): # над отестить оптимальное количество баллов
            team_ball = 12
        elif (total_day <=99) and (total_day>=90):
            team_ball = 9
        elif (total_day <= 89) and (total_day> 80):
            team_ball = 8
        elif (total_day < 79) and (total_day> 70):
            team_ball = 7
        elif (total_day < 69) and (total_day> 60):
            team_ball = 6
        elif (total_day < 59) and (total_day> 50):
            team_ball = 5
        else:
            team_ball=0
        return team_ball

    def sumar_mons_balls(self,team_ball):
        summ_team_balls=0
        summ_team_balls=summ_team_balls+team_ball
        return summ_team_balls
