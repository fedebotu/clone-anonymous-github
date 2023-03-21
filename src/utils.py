import threading
import ctypes

class ThreadWithException(threading.Thread):
    """Thread class throwing an exception when stopped"""
    def __init__(self, target, args):
        threading.Thread.__init__(self)
        self.target = target
        self.args = args
        self.return_value = None # return value of target function
             
    def run(self):
        self.return_value = self.target(*self.args)

    def get_id(self):
 
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
  
    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')