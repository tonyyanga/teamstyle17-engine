# Source Generated with Decompyle++
# File: uiobj.pyc (Python 3.4)

import main
import action
import queue
import socket
import json
import threading

def RecvThread():
    '''RecvThread'''
    __qualname__ = 'RecvThread'
    
    def __init__(self, sock, signal_queue, queue_function, bufsize = 4096):
        threading.Thread.__init__(self)
        self.socket = sock
        self.queue_function = queue_function
        self.bufsize = bufsize
        self._send_signal_queue = signal_queue
        self.sig = queue.Queue()

    
    def run(self):
        buf = ''
        while None:
            
            try:
                data = self.socket.recv(self.bufsize).decode()
            except UnicodeDecodeError:
                e = None
                
                try:
                    main.root_logger.error('platform (UI) exception %s [%s]', type(e).__name__, str(e))
                finally:
                    e = None
                    del e

            except OSError:
                break

            if data == '':
                break
            if data is not None:
                buf += data
                b = buf.find('{')
                if b < 0:
                    buf = ''
                else:
                    buf = buf[b:]
            e = buf.find('}')
            while e >= 0:
                self.queue_function(buf[:e + 1])
                b = buf.find('{', e + 1)
                if b < 0:
                    buf = ''
                else:
                    buf = buf[b:]
                e = buf.find('}')
            continue
        self._send_signal_queue.put(1)


RecvThread = <NODE:28>(RecvThread, 'RecvThread', threading.Thread)

def SendThread():
    '''SendThread'''
    __qualname__ = 'SendThread'
    
    def __init__(self, sock, signal_queue):
        threading.Thread.__init__(self)
        self.socket = sock
        self._send_signal_queue = signal_queue
        self.sig = queue.Queue()

    
    def run(self):
        while None:
            q = self.sig.get(block = True)
            if q == 0:
                break
                continue
            data_type = ''
            
            try:
                j = json.loads(q)
                if type(j) == dict:
                    if j.get('players') is not None:
                        data_type = 'query_status'
                    elif j.get('objects') is not None:
                        data_type = 'query_map'
                    
                if type(j) == list:
                    data_type = 'info_add'
            except ValueError:
                pass

            if data_type != '':
                q = load_msg_from_logic(q, data_type)
            if not q.endswith('\n'):
                q += '\n'
            
            try:
                self.socket.send(q.encode())
            continue
            except BrokenPipeError:
                break
                continue
                except OSError:
                    break
                    continue
                
            return None



SendThread = <NODE:28>(SendThread, 'SendThread', threading.Thread)

def load_msg_from_logic(msg = None, action_name = None):
    skill_types = [
        'longAttack',
        'shortAttack',
        'shield',
        'dash',
        'visionUp',
        'healthUp']
    object_types = [
        'player',
        'food',
        'nutrient',
        'spike',
        'target',
        'bullet',
        'source']
    info_types = [
        'object',
        'delete',
        'player',
        'skill_cast',
        'skill_hit',
        'end']
    ret_str = ''
    ret_str_list = []
    
    try:
        if action_name == 'query_status':
            ret_str_list.append('s')
            info = json.loads(msg)
            ret_str_list.append('%d|' % info['time'])
            for player in info['players']:
                skill_levels = [
                    0] * 6
                skill_cds = [
                    -1] * 6
                for skill in player['skills']:
                    index = skill_types.index(skill['name'])
                    skill_levels[index] = skill['level']
                    skill_cds[index] = skill['cd']
                
                s = '%d %d %d %d %d %d %.10f %.10f %.10f %.10f %.10f %.10f %.10f %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d;' % (player['id'], player['ai_id'], player['health'], player['max_health'], player['vision'], player['ability'], player['r'], player['pos'][0], player['pos'][1], player['pos'][2], player['speed'][0], player['speed'][1], player['speed'][2], skill_levels[0], skill_levels[1], skill_levels[2], skill_levels[3], skill_levels[4], skill_levels[5], skill_cds[0], skill_cds[1], skill_cds[2], skill_cds[3], skill_cds[4], skill_cds[5], player['longattackcasting'], player['shieldtime'], player['dashtime'])
                ret_str_list.append(s)
            
            ret_str = '\ns'.join(ret_str_list) + '#\n'
        elif action_name == 'query_map':
            ret_str_list.append('m')
            info = json.loads(msg)
            ret_str_list.append('%d|' % info['time'])
            for obj in info['objects']:
                s = '%d %d %d %.10f %.10f %.10f %.10f %d %d;' % (int(obj['id']), int(obj['ai_id']), int(object_types.index(obj['type'])), obj['pos'][0], obj['pos'][1], obj['pos'][2], obj['r'], obj['longattackcasting'], obj['shieldtime'])
                ret_str_list.append(s)
            
            ret_str = '\nm'.join(ret_str_list) + '#\n'
        elif action_name == 'info_add':
            ret_str_list.append('a')
            info_list = json.loads(msg)
            for info in info_list:
                if info['info'] == 'object':
                    s = '%d %d %d %d %d %.10f %.10f %.10f %.10f %d %d %d;' % (info_types.index(info['info']), info['time'], info['id'], info['ai_id'], object_types.index(info['type']), info['pos'][0], info['pos'][1], info['pos'][2], info['r'], -1, 0, info['nutrientmove'])
                    ret_str_list.append(s)
                elif info['info'] == 'delete':
                    s = '%d %d %d;' % (info_types.index(info['info']), info['time'], info['id'])
                    ret_str_list.append(s)
                elif info['info'] == 'player':
                    skill_levels = [
                        -1] * 6
                    skill_cds = [
                        -1] * 6
                    for skill in info['skills']:
                        index = skill_types.index(skill['name'])
                        skill_levels[index] = skill['level']
                        skill_cds[index] = skill['cd']
                    
                    s = '%d %d %d %d %d %d %d %d %.10f %.10f %.10f %.10f %.10f %.10f %.10f %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d;' % (info_types.index(info['info']), info['time'], info['id'], info['ai_id'], info['health'], info['max_health'], info['vision'], info['ability'], info['r'], info['pos'][0], info['pos'][1], info['pos'][2], info['speed'][0], info['speed'][1], info['speed'][2], skill_levels[0], skill_levels[1], skill_levels[2], skill_levels[3], skill_levels[4], skill_levels[5], skill_cds[0], skill_cds[1], skill_cds[2], skill_cds[3], skill_cds[4], skill_cds[5], info['longattackcasting'], info['shieldtime'], info['dashtime'])
                    ret_str_list.append(s)
                elif info['info'] == 'skill_cast':
                    if not info.get('x'):
                        pass
                    if not info.get('y'):
                        pass
                    if not info.get('z'):
                        pass
                    s = '%d %d %d %d %d %.10f %.10f %.10f;' % (info_types.index(info['info']), info['time'], info['source'], skill_types.index(info['type']), -1, 0, 0, 0)
                    ret_str_list.append(s)
                elif info['info'] == 'skill_hit':
                    s = '%d %d %d %d %d;' % (info_types.index(info['info']), info['time'], skill_types.index(info['type']), info['player'], info['target'])
                    ret_str_list.append(s)
                elif info['info'] == 'end':
                    s = '%d %d %d;' % (info_types.index(info['info']), info['time'], info['ai_id'])
                    ret_str_list.append(s)
                ret_str = '\na'.join(ret_str_list) + '#\n'
            
    except KeyError:
        err = None
        
        try:
            main.root_logger.error('platform (UI) exception %s [%s]' % (type(err).__name__, str(err)))
            ret_str = '\n'
        finally:
            err = None
            del err


    return ret_str


def UIObject():
    '''UIObject'''
    __qualname__ = 'UIObject'
    
    def __init__(self, game, host = 'localhost', port = 6000, backlog = 1, ai_id = -1):
        threading.Thread.__init__(self)
        self.socket = socket.socket()
        self.socket.bind((host, port))
        self.socket.listen(backlog)
        self.sig = queue.Queue()
        self.recv_thread = None
        self.send_thread = None
        self.ui_socket = None
        self._game_obj = game
        self._ai_id = ai_id

    
    def exit(self):
        self.socket.close()
        self.sig.put(0)
        self._UIObject__exit_child_threads()

    
    def _UIObject__exit_child_threads(self):
        if self.ui_socket:
            self.ui_socket.close()
        if self.recv_thread and self.recv_thread.is_alive():
            self.recv_thread.sig.put(0)
        if self.send_thread and self.send_thread.is_alive():
            self.send_thread.sig.put(0)
        if self.recv_thread:
            self.recv_thread.join()
        if self.send_thread:
            self.send_thread.join()

    
    def push_queue_ui(self = None, obj = None):
        json_obj = json.loads(obj)
        act = json_obj.get('action')
        if not json_obj.get('time'):
            pass
        timestamp = self._game_obj.current_time
        if act and act[0] == '_':
            self._game_obj.enqueue(timestamp, action.Action('{"action":"_platform","ai_id":%d}' % self._ai_id, act, self.send_thread.sig))
        else:
            self._game_obj.enqueue(timestamp, action.Action(obj, 'query', self.send_thread.sig))

    
    def enqueue(self = None, data = None):
        if not type(data) == str:
            raise AssertionError
        if None.send_thread and self.send_thread.is_alive():
            self.send_thread.sig.put(data)

    
    def run(self):
        self.sig.put(2)
        while None:
            q = self.sig.get(block = True)
            if q == 0:
                break
            if q == 1:
                main.root_logger.info('platform (UI) Connection reset by peer.')
                self._UIObject__exit_child_threads()
            
            try:
                (self.ui_socket, address) = self.socket.accept()
                main.root_logger.info('platform (UI) Connection accepted from %s', repr(address))
                self.sig = queue.Queue()
                self.send_thread = SendThread(self.ui_socket, self.sig)
                self.send_thread.start()
                self.recv_thread = RecvThread(self.ui_socket, self.sig, self.push_queue_ui)
                self.recv_thread.start()
            continue
            except OSError:
                break
                continue
            



UIObject = <NODE:28>(UIObject, 'UIObject', threading.Thread)
