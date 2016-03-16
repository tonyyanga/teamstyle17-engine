# Source Generated with Decompyle++
# File: scene.pyc (Python 3.4)

import copy

class Sphere:
    __qualname__ = 'Sphere'
    
    def __init__(self = None, center = None, r = None):
        self.center = center
        self.radius = r



class Octree:
    __qualname__ = 'Octree'
    
    class OctreeNode:
        __qualname__ = 'Octree.OctreeNode'
        _nodeSizeLimit = 4
        
        def __init__(self):
            self.smallCorner = (0, 0, 0)
            self.bigCorner = (0, 0, 0)
            self.fixedObjList = []
            self.pushableObjList = []
            self.children = []

        
        def center(self):
            return (tuple,)(lambda .0: continue(range(3)))

        
        def sideLength(self):
            return self.bigCorner[0] - self.smallCorner[0]

        
        def _makeChildren(self):
            center = self.center()
            self.children = []
            for newNode in range(0, 8):
                i = None
                newCorner = (None, tuple)(lambda .0: continue(range(3)))
                newNode.smallCorner = (None, tuple)(lambda .0: continue(range(3)))
                newNode.bigCorner = (None, tuple)(lambda .0: continue(range(3)))
                self.children.append(newNode)
            

        
        def _pushCode(self = None, obj = None):
            center = self.center()
            if (None, any)(lambda .0: continue(range(3))):
                return -1
            return (None, None)(lambda .0: continue(range(3)))

        
        def insert(self = None, objId = None, tree = None):
            obj = tree._objs.get(objId)
            code = self._pushCode(obj)
            if code == -1:
                self.fixedObjList.append(objId)
            else:
                self.pushableObjList.append(objId)
            self._pushIfNecessary(tree)

        
        def _pushIfNecessary(self, tree):
            if len(self.pushableObjList) == 0 or len(self.fixedObjList) + len(self.pushableObjList) <= self._nodeSizeLimit:
                return None
            if None(self.children) == 0:
                self._makeChildren()
            for objId in self.pushableObjList:
                code = self._pushCode(tree._objs[objId])
                tree._paths[objId] += str(code)
                self.children[code].insert(objId, tree)
            
            self.pushableObjList = []

        
        def delete(self = None, objId = None, route = None):
            if route == '':
                
                try:
                    self.fixedObjList.remove(objId)
                except:
                    pass

                
                try:
                    self.pushableObjList.remove(objId)

            else:
                self.children[int(route[0])].delete(objId, route[1:])

        
        def intersect(self = None, obj = None, tree = None, centerOnly = None):
            
            def dist(p1 = None, p2 = None):
                return (None, sum)(lambda .0: continue(range(3))) ** 0.5

            
            def insideSphere(obj = None, point = None):
                return dist(obj.center, point) < obj.radius

            
            def intersectWithSphere(obj1 = None, obj2 = None):
                return dist(obj1.center, obj2.center) < obj1.radius + obj2.radius

            
            def intersectWithBox(obj = None, small = None, big = None):
                dist2 = obj.radius ** 2
                for i in range(3):
                    if obj.center[i] < small[i]:
                        dist2 -= (obj.center[i] - small[i]) ** 2
                        continue
                    if obj.center[i] > big[i]:
                        dist2 -= (big[i] - obj.center[i]) ** 2
                        continue
                return dist2 > 0

            if centerOnly:
                pass
            ans = None(((None, list, filter), lambda objId: insideSphere(obj, tree._objs[objId].center), 1)(lambda objId: intersectWithSphere(obj, tree._objs[objId]), self.fixedObjList + self.pushableObjList))
            if len(self.children) > 0:
                for ch in self.children:
                    if intersectWithBox(obj, ch.smallCorner, ch.bigCorner):
                        ans.extend(ch.intersect(obj, tree, centerOnly))
                
            return ans


    
    def __init__(self, mapSize = 1000000):
        self._root = self.OctreeNode()
        self._root.bigCorner = (mapSize, mapSize, mapSize)
        self._objs = { }
        self._paths = { }

    
    def insert(self = None, obj = None, objId = None):
        if self._objs.get(objId) is not None:
            raise ValueError
        self._objs[objId] = copy.copy(obj)
        self._paths[objId] = ''
        self._root.insert(objId, self)

    
    def getObject(self = None, objId = None):
        return copy.copy(self._objs.get(objId))

    
    def modify(self = None, obj = None, objId = None):
        if self._objs.get(objId) is None:
            raise ValueError
        self._root.delete(objId, self._paths[objId])
        self._objs[objId] = copy.copy(obj)
        self._paths[objId] = ''
        self._root.insert(objId, self)

    
    def delete(self = None, objId = None):
        self._root.delete(objId, self._paths[objId])
        self._objs.pop(objId)
        self._paths.pop(objId)

    
    def intersect(self = None, obj = None, centerOnly = None):
        return self._root.intersect(obj, self, centerOnly)


