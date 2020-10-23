from multiprocessing import Process


def func():
    print("i am subprocess")


new_process = Process(target=func)
print("i am Parent Process")
