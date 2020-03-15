#!/usr/bin/env python2.7

import sys
import random
import time
import datetime
import argparse
import threading
import signal
import os

ADD = 0 
SUB = 1
MUL = 2
DIV = 3
RANDOM = 4

class test_report():
    def __init__(self, timeout_period, num_q):
        self.start_time = datetime.datetime.now()
        self.timeout_duration = timeout_period
        self.num_q = num_q
        self.score = 0

    def increse_score(self):
        self.score = self.score + 1

    def time_taken(self):
        now = datetime.datetime.now()
        return now - self.start_time

    def get_score(self):
        return self.score

    def print_report(self):
        time_taken = int(self.time_taken().total_seconds())
        minutes = int(time_taken / 60)
        seconds = int(time_taken % 60)

        if self.timeout_duration:
            if time_taken > self.timeout_duration:
                print("\n\n==============================================")
                time_exceeded = time_taken - self.timeout_duration
                time_exceeded_minutes = int(time_exceeded / 60)
                time_exceeded_seconds = int(time_exceeded % 60)
                print('Time exceeded by minutes {} seconds: {}'.format(
                    time_exceeded_minutes, time_exceeded_seconds))

        print("\n\n==============================================")
        print('Test Finished! time: {}'.format(
            datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        print("Minutes: {0} Seconds: {1}".format(minutes, seconds))
        print("=================================================")
        print("\nScore:\nCorrect: {0} Wrong: {1}".format(
            self.get_score(), self.num_q-self.get_score()))
        print("=================================================")

    def test_end(self):
        self.print_report
        sys.exit(0)

class thread_timer(threading.Thread):
    def __init__(self, timeout_duration):
        threading.Thread.__init__(self)
        self.timeout_duration = timeout_duration
        self.kill_received = False

    def run(self):
        print 'Starting timer for {} sec'.format(self.timeout_duration)
        self.active = True
        while ((not self.kill_received) and (self.timeout_duration)):
            time.sleep(1)
            self.timeout_duration -=1
        self.active = False

        if self.timeout_duration == 0:
            try:
                raise TimerTimedOut
            except TimerTimedOut as timeout:
                print '\n**** TIMEOUT ****'


    def alive(self):
        return self.active

    def cancel(self):
        print 'Stopping the timer'
        self.kill_received = True


class TestExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


def test_stop(signum, frame):
    #print('Caught signal %d' % signum)
    raise TestExit

class TimerTimedOut(Exception):
    pass

def test(q_type, num_q, q_level, timeout_period):

    signal.signal(signal.SIGTERM, test_stop)
    signal.signal(signal.SIGINT, test_stop)

    oper = q_type
    if timeout_period:
        timeout_period = timeout_period * 60

    # Convert minutes to seconds
    report = test_report(timeout_period, num_q)

    if timeout_period:
        timer = thread_timer(timeout_period)
        try:
            timer.start()
        except Exception, e:
            print 'Exception: {}'.format(e)

    print('\n\n*** Test started! time: {} ***\n'.format(
        datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))


    rand_oper_start = ADD 
    rand_oper_end = DIV 

    if q_level == 'basic':
        add_operand1_min = 0;
        add_operand1_max = 10;
        add_operand2_min = 0;
        add_operand2_max = 10;

        sub_operand1_min = 0;
        sub_operand1_max = 10;
        sub_operand2_min = 0;
        sub_operand2_max = 10;

        mul_operand1_min = 0;
        mul_operand1_max = 10;
        mul_operand2_min = 0;
        mul_operand2_max = 10;

        dev_operand1_min = 1;
        dev_operand1_max = 10;
        dev_operand2_min = 0;
        dev_operand2_max = 10;
    elif q_level == 'medium':
        add_operand1_min = 1;
        add_operand1_max = 100;
        add_operand2_min = 1;
        add_operand2_max = 100;

        sub_operand1_min = 1;
        sub_operand1_max = 100;
        sub_operand2_min = 0;
        sub_operand2_max = 100;

        mul_operand1_min = 1;
        mul_operand1_max = 20;
        mul_operand2_min = 1;
        mul_operand2_max = 10;

        dev_operand1_min = 3;
        dev_operand1_max = 20;
        dev_operand2_min = 4;
        dev_operand2_max = 10;
    elif q_level == 'high':
        add_operand1_min = 1;
        add_operand1_max = 10000;
        add_operand2_min = 1;
        add_operand2_max = 10000;

        sub_operand1_min = 1;
        sub_operand1_max = 10000;
        sub_operand2_min = 0;
        sub_operand2_max = 10000;

        mul_operand1_min = 0;
        mul_operand1_max = 1000;
        mul_operand2_min = 0;
        mul_operand2_max = 1000;

        dev_operand1_min = 1;
        dev_operand1_max = 1000;
        dev_operand2_min = 0;
        dev_operand2_max = 1000;
    else:
        print 'Invalid question level: {}'.format(q_level)
        sys.exit(1)

    try:
        for i in range(num_q):
            if q_type == RANDOM:
                oper = random.randint(rand_oper_start, rand_oper_end)

            if oper == ADD:
                x = random.randint(add_operand1_min, add_operand1_max)
                y = random.randint(add_operand2_min, add_operand2_max)
                answer = x + y
                oper_str = "+"
            elif oper == SUB:
                x = random.randint(sub_operand1_min, sub_operand1_max)
                y = random.randint(sub_operand2_min, x)
                answer = x - y
                oper_str = "-"
            elif oper == MUL:
                x = random.randint(mul_operand1_min, mul_operand1_max)
                y = random.randint(mul_operand2_min, mul_operand2_max)
                answer = x * y
                oper_str = "x"
            elif oper == DIV:
                y = random.randint(dev_operand1_min, dev_operand1_max)
                answer = random.randint(dev_operand2_min, dev_operand2_max)
                x = y * answer
                oper_str = "/"
            else:
                print("Invalid operation type!");

            while True:
                try:
                    n = int(raw_input(
                        "\nQuestion {0}\n{1} {2} {3} = ".format(
                            i+1, x, oper_str, y)))
                    break
                except TestExit as test_exit:
                    report.print_report()
                    if timeout_period:
                        timer.cancel()
                    sys.exit(1)
                except TimerTimedOut as timeout:
                    print 'TIMEOUT!'
                    report.print_report()
                    if timeout_period:
                        timer.cancel()
                    sys.exit(1)
                except ValueError as verr:
                    print("Inavalid number! Enter correct number!")
                except Exception as ex:
                    print("Inavalid number! Enter correct number!")

            if answer == n:
                print("Great..Answer is correct!!!")
                report.increse_score()
            else:
                print("Sorry...Answer is Wrong. Correct answer is {0}".format(answer))
    except KeyboardInterrupt:
        # Ctrl-C handling and send kill to threads
        print 'Test is killed!'
        if timeout_period:
            timer.cancel()

    report.print_report()
    if timeout_period:
        timer.cancel()
    sys.exit(0)

def time_duration(x):
    x = int(x)
    if ((x < 1) or (x > 120)):
        raise argparse.ArgumentTypeError('Invalid time duration for the test! Valid duration is 1 to 120 minutes.')
    return x

def main():
    arg_parser = argparse.ArgumentParser(description = 'Welcome to nMath')
    parser = arg_parser.add_mutually_exclusive_group(required=True)
    parser.add_argument("-m", help="Multiplications", dest='mul', action="store_true")
    parser.add_argument("-a", help="Additions", dest='add', action="store_true")
    parser.add_argument("-s", help="Suntractions", dest='sub', action="store_true")
    parser.add_argument("-d", help="Divisions", dest='div', action="store_true")
    parser.add_argument("-r", help="Random questions", dest='random', action="store_true")
    arg_parser.add_argument("-n", help="Number of questions", dest="num_q", required=True, type=int, choices=[5, 10, 20, 40, 50, 100, 200])
    arg_parser.add_argument("-t", help="time duration in minutes", dest="time_duration", type=time_duration)
    arg_parser.add_argument("-l", help="Level of difficulty", dest="level", required=True, choices=['basic', 'medium', 'high'])

    args = arg_parser.parse_args()

    # print args

    if args.add:
        test(ADD, args.num_q, args.level, args.time_duration)
    elif args.sub:
        test(SUB, args.num_q, args.level, args.time_duration)
    elif args.mul:
        test(MUL, args.num_q, args.level, args.time_duration)
    elif args.div:
        test(DIV, args.num_q, args.level, args.time_duration)
    elif args.random:
        test(RANDOM, args.num_q, args.level, args.time_duration)

if __name__ == '__main__':
    main()

