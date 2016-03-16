# Source Generated with Decompyle++
# File: gamemain.pyc (Python 3.4)

from ts17core import scene, myrand

class PlayerStatus:
    __qualname__ = 'PlayerStatus'
    
    def __init__(self):
        self.aiId = 0
        self.health = 0
        self.speed = (0, 0, 0)
        self.speedLimit = 100
        self.ability = 0
        self.vision = 5000
        self.skillsLV = { }
        self.skillsCD = { }
        self.longAttackCasting = -1
        self.longAttackEnemy = -1
        self.dashTime = 0
        self.shieldTime = 0
        self.shieldLevel = 0
        self.stopTime = 0
        self.maxHealth = self.health
        self.nutrientMove = 0

    
    def healthChange(self, delta):
        self.health += delta
        if self.health > self.maxHealth:
            self.maxHealth = self.health



class ObjectStatus:
    __qualname__ = 'ObjectStatus'
    
    def __init__(self, objType = 'food'):
        self.type = objType



class BulletStatus:
    __qualname__ = 'BulletStatus'
    
    def __init__(self = None, damage = None, enemy = None, speed = None, owner = None, stop = None):
        self.type = 'bullet'
        self.damage = damage
        self.enemy = enemy
        self.owner = owner
        self.stop = stop
        self.speed = speed



class CastSkillInfo:
    __qualname__ = 'CastSkillInfo'
    
    def __init__(self, name):
        self.name = name



class CastLongAttackInfo:
    __qualname__ = 'CastLongAttackInfo'
    
    def __init__(self, tPlayer):
        self.name = 'longAttack'
        self.player = tPlayer



class GameMain:
    __qualname__ = 'GameMain'
    
    def __init__(self, seed, playerNum, type, callback):
        self._gameEnd = False
        self.gameType = type
        self._mapSize = 20000
        self._time = 0
        self._players = { }
        self._objects = { }
        self._callback = callback
        self._scene = scene.Octree(self._mapSize)
        self._castSkills = { }
        self._rand = myrand.MyRand(seed)
        self._skillPrice = {
            'longAttack': 1,
            'shortAttack': 1,
            'shield': 2,
            'dash': 2,
            'visionUp': 2,
            'healthUp': 1 }
        self._foodCount = 0
        self._foodCountAll = 0
        self._spikeCount = 0
        self._spikeCountAll = 0
        self._nutrientFlushTime = 0
        self._nutrientFlushPos = []
        for x in range(8):
            temp = x
            for _ in range(5):
                None((self._nutrientFlushPos.append, tuple)(lambda .0: continue(range(3))))
            
        
        self._changeList = []
        self._changedPlayer = set()
        self.addNewPlayer(0, -2, (tuple,)(lambda .0: continue(range(3))), 2000)
        pos1 = (tuple,)(lambda .0: continue(range(3)))
        pos2 = (None, tuple)(lambda .0: continue(range(3)))
        self.addNewPlayer(1, 0, pos1, 1000)
        self.addNewPlayer(2, 1, pos2, 1000)

    
    def playerPos(self, playerId):
        return self._scene.getObject(playerId).center

    
    def addNewPlayer(self = None, playerId = None, aiId = None, pos = None, radius = None):
        sphere = scene.Sphere(pos, radius)
        self._scene.insert(sphere, playerId)
        newStatus = PlayerStatus()
        newStatus.health = int((radius / 100) ** 3)
        newStatus.maxHealth = newStatus.health
        newStatus.aiId = aiId
        self._players[playerId] = newStatus

    
    def makeChangeJson(self = None, playerId = None, aiId = None, pos = None, r = None, nutrientMove = None):
        if self._objects.get(playerId) is not None:
            objType = self._objects[playerId].type
        elif self._players.get(playerId) is not None:
            objType = 'player'
        else:
            objType = None
        return '{"info":"object","time":%d,"id":%d,"ai_id":%d,"type":"%s","pos":[%.10f,%.10f,%.10f],"r":%.10f,"nutrientmove":%d}' % (self._time, playerId, aiId, objType, pos[0], pos[1], pos[2], r, nutrientMove)

    
    def makeDeleteJson(self = None, objId = None):
        return '{"info":"delete","time":%d,"id":%d}' % (self._time, objId)

    
    def makeSkillCastJson(self = None, source = None, skillType = None, target = None):
        if target is not None:
            targetStr = ',"target":%d' % target
        else:
            targetStr = ''
        return '{"info":"skill_cast","time":%d,"source":%d,"type":"%s"%s}' % (self._time, source, skillType, targetStr)

    
    def makeSkillHitJson(self = None, skillType = None, player = None, target = None):
        return '{"info":"skill_hit","time":%d,"type":"%s","player":%d,"target":%d}' % (self._time, skillType, player, target)

    
    def makePlayerJson(self = None, playerId = None):
        player = self._players[playerId]
        skillList = (','.join,)(lambda .0: continue(player.skillsLV.keys()))
        speedStr = ','.join(lambda .0: continue(player.speed))
        sphere = self._scene.getObject(playerId)
        pos = ','.join(lambda .0: continue(sphere.center))
        return '{"info":"player","time":%d,"id":%d,"ai_id":%d,"health":%d,"max_health":%d,"vision":%d,"ability":%d,"pos":[%s],"r":%d,"longattackcasting":%d,"shieldtime":%d,"dashtime":%d,"speed":[%s],"skills":[%s]}' % (self._time, playerId, player.aiId, player.health, player.maxHealth, player.vision, player.ability, pos, sphere.radius, player.longAttackCasting, player.shieldTime, player.dashTime, speedStr, skillList)

    
    def update(self):
        self._changeList = []
        self._changedPlayer = set()
        if self._time == 5000:
            tempId = 0
            tempMax = 0
            for playerId in self._players:
                if self._players[playerId].aiId == -2:
                    continue
                if self._players[playerId].health > tempMax:
                    tempMax = self._players[playerId].health
                    tempId = self._players[playerId].aiId
                    continue
            self.gameEnd(tempId, 1)
        for playerId in self._rand.shuffle(list(self._castSkills.keys())):
            if self._players.get(playerId) is None:
                continue
            skillInfo = self._castSkills[playerId]
            skillName = skillInfo.name
            if skillName == 'shortAttack':
                self.shortAttack(playerId)
                continue
            if skillName == 'longAttack':
                self.longAttackSet(playerId, skillInfo.player)
                continue
            if skillName == 'dash':
                self.dash(playerId)
                continue
            if skillName == 'shield':
                self.shield(playerId)
                continue
            if skillName == 'visionUp':
                self.visionUp(playerId)
                continue
            if skillName == 'healthUp':
                self.healthUp(playerId)
                continue
        for (playerId, player) in self._players.items():
            if player.longAttackCasting == 0:
                self.longAttackDone(playerId)
            if player.dashTime == 0:
                player.speedLimit = 100
                continue
        self._castSkills.clear()
        for (playerId, player) in self._players.items():
            if playerId == 0:
                player.speed = (tuple,)(lambda .0: continue(range(3)))
            if player.stopTime == 0:
                self.playerMove(playerId)
                continue
        for playerId in self._rand.shuffle(list(self._players.keys())):
            player = self._players.get(playerId)
            if player is None:
                continue
            sphere = self._scene.getObject(playerId)
            insideList = self._scene.intersect(sphere, True)
            eatableList = lambda .0: for objId in .0:
if 1.2 * self._scene._objs[objId].radius < sphere.radius:
continue[][objId](insideList)
            for eatenId in eatableList:
                self._changeList.append(self.makeDeleteJson(eatenId))
                eatenPlayer = self._players.get(eatenId)
                if eatenPlayer is not None:
                    if not eatenPlayer.shieldTime == 0:
                        if eatenPlayer.skillsLV['shield'] < 4 and eatenPlayer.shieldLevel < 5 or player.aiId == -2:
                            self.gameEnd(1 - eatenPlayer.aiId, 2)
                        else:
                            self.gameEnd(self._players[playerId].aiId, 3)
                        continue
                objType = self._objects[eatenId].type
                if objType == 'food':
                    self.healthChange(playerId, 40)
                    self.objectDelete(eatenId)
                    self._foodCount -= 1
                    continue
                if objType == 'nutrient':
                    player.ability += self._rand.rand() % 5 + 1
                    self.nutrientMove(playerId)
                    self.objectDelete(eatenId)
                    continue
            if playerId == 0:
                continue
            if self._players[playerId].nutrientMove > 0:
                continue
            touchList = self._scene.intersect(sphere, False)
            for touchedId in touchList:
                if self._players.get(touchedId) is not None:
                    continue
                objType = self._objects[touchedId].type
                if (objType == 'spike' or self._players[playerId].shieldTime == 0 or self._players[playerId].skillsLV['shield'] < 5) and self._players[playerId].shieldLevel < 5:
                    damage = self._players[playerId].health // 3
                    self.healthChange(playerId, -damage)
                    self.objectDelete(touchedId)
                
            
        
        if self._time == 0:
            foodPerTick = 150
        else:
            foodPerTick = 10
        for _ in range(foodPerTick):
            if self._foodCount > 300:
                break
            center = (tuple,)(lambda .0: continue(range(3)))
            food = scene.Sphere(center)
            foodId = 1000000 + self._foodCountAll
            self._objects[foodId] = ObjectStatus('food')
            self._scene.insert(food, foodId)
            self._foodCountAll += 1
            self._foodCount += 1
            self._changeList.append(self.makeChangeJson(foodId, -2, center, 0))
        
        spikenum = 0
        if self._time % 100 == 0:
            spikenum += 1
        for _ in range(spikenum):
            if self._spikeCount >= 10:
                break
            center = (tuple,)(lambda .0: continue(range(3)))
            spike = scene.Sphere(center)
            spikeId = 2001000 + self._spikeCountAll
            self._objects[spikeId] = ObjectStatus('spike')
            self._scene.insert(spike, spikeId)
            self._spikeCountAll += 1
            self._spikeCount += 1
            self._changeList.append(self.makeChangeJson(spikeId, -2, center, 0))
        
        if self._nutrientFlushTime == 0:
            pos = self._rand.randIn(len(self._nutrientFlushPos))
            nutrientId = int(2000000 + pos)
            time = 0
            while self._objects.get(nutrientId) is not None:
                pos = self._rand.randIn(len(self._nutrientFlushPos))
                nutrientId = int(2000000 + pos)
                time += 1
                if time > 10:
                    break
                    continue
                if time <= 10:
                    nutrient = scene.Sphere(self._nutrientFlushPos[pos])
                    self._objects[nutrientId] = ObjectStatus('nutrient')
                    self._scene.insert(nutrient, nutrientId)
                    self._nutrientFlushTime = self._rand.randIn(100) + 10
                
        self._nutrientFlushTime -= 1
        self._time += 1
        for (playerId, player) in self._players.items():
            if player.shieldTime > 0:
                player.shieldTime -= 1
            if player.shieldLevel > 0:
                player.shieldLevel -= 1
            if player.stopTime > 0:
                player.stopTime -= 1
            if player.longAttackCasting > 0:
                player.longAttackCasting -= 1
            if player.dashTime > 0:
                player.dashTime -= 1
            if player.nutrientMove > 0:
                player.nutrientMove -= 1
            for skillName in self._players[playerId].skillsCD.keys():
                if player.skillsCD[skillName] > 0:
                    player.skillsCD[skillName] -= 1
                    continue
        
        for playerId in self._changedPlayer:
            if self._players.get(playerId) is not None:
                self._changeList.append(self.makePlayerJson(playerId))
                continue
        if self.gameType != 0 and self.gameType == 1:
            for playerId in self._players:
                if self._players[playerId].aiId != 0:
                    continue
                if self._players[playerId].speed != (0, 0, 0):
                    self.testGameEnd(10)
                    continue
        self._callback('[' + ','.join(self._changeList) + ']')

    
    def healthChange(self = None, playerId = None, delta = None):
        player = self._players.get(playerId)
        if player is None:
            raise ValueError('Player %d does not exist' % playerId)
        player.healthChange(delta)
        newHealth = player.health
        if newHealth < player.maxHealth // 4:
            self.playerDie(playerId)
        else:
            newRadius = newHealth ** 0.333333 * 100
            newSphere = scene.Sphere(self._scene.getObject(playerId).center, newRadius)
            self._scene.modify(newSphere, playerId)
            self._changedPlayer.add(playerId)

    
    def playerDie(self = None, playerId = None):
        player = self._players.get(playerId)
        if player is None:
            raise ValueError('Player %d does not exist' % playerId)
        if player.health > player.maxHealth // 4:
            raise ValueError('This player is still alive')
        self._players.pop(playerId)
        self._scene.delete(playerId)
        self._changeList.append(self.makeDeleteJson(playerId))
        aliveAI = set()
        for player in self._players.values():
            if player.aiId >= 0:
                aliveAI.add(player.aiId)
                continue
        if len(aliveAI) == 1:
            self.gameEnd(aliveAI.pop(), 4)

    
    def objectDelete(self = None, objId = None):
        obj = self._objects.get(objId)
        if obj is None:
            raise ValueError('Object %d does not exist' % objId)
        self._objects.pop(objId)
        self._scene.delete(objId)
        self._changeList.append(self.makeDeleteJson(objId))

    
    def playerMove(self = None, playerId = None):
        oldPos = self._scene.getObject(playerId).center
        r = self._scene.getObject(playerId).radius
        speed = self._players[playerId].speed
        newPos = (None, tuple)(lambda .0: continue(range(3)))
        if self.outsideMap(newPos, r):
            newPos2 = list(newPos)
            for i in range(3):
                if newPos2[i] + r > self._mapSize:
                    newPos2[i] = self._mapSize - r
                    continue
                if newPos[i] - r < 0:
                    newPos2[i] = r
                    continue
            newPos = tuple(newPos2)
        newSphere = scene.Sphere(newPos, r)
        self._scene.modify(newSphere, playerId)
        self._changeList.append(self.makeChangeJson(playerId, self._players[playerId].aiId, newSphere.center, newSphere.radius))

    
    def isBelong(self = None, playerId = None, aiId = None):
        player = self._players.get(playerId)
        if player is None:
            raise ValueError('Player %d does not exist' % playerId)
        return player.aiId == aiId

    
    def getFieldJson(self = None, aiId = None):
        
        def makeObjectJson(objId, aiId, objType, pos, r, longAttackCasting = -1, shieldTime = -1):
            return '{"id":%d,"ai_id":%d,"type":"%s","pos":[%.10f,%.10f,%.10f],"r":%.10f,"longattackcasting":%d,"shieldtime":%d}' % (objId, aiId, objType, pos[0], pos[1], pos[2], r, longAttackCasting, shieldTime)

        objectDict = { }
        if aiId == -1:
            for playerId in self._players:
                sphere = self._scene.getObject(playerId)
                objectDict[playerId] = makeObjectJson(playerId, self._players[playerId].aiId, 'player', sphere.center, sphere.radius, self._players[playerId].longAttackCasting, self._players[playerId].shieldTime)
            
            for objectId in self._objects:
                status = self._objects[objectId]
                sphere = self._scene._objs[objectId]
                objectDict[objectId] = makeObjectJson(objectId, -2, status.type, sphere.center, sphere.radius)
            
            for nutrientId in enumerate(self._nutrientFlushPos):
                (i, pos) = None
                objectDict[nutrientId] = makeObjectJson(nutrientId, -2, 'source', pos, 0)
            
        else:
            visionSpheres = lambda .0: for playerId in .0:
if self._players[playerId].aiId == aiId:
continue[][scene.Sphere(self._scene.getObject(playerId).center, self._players[playerId].vision)](self._players.keys())
            visibleLists = lambda .0: continue[ self._scene.intersect(vs, False) for vs in .0 ](visionSpheres)
            for objectId in lambda .0: continue[ i for ls in .0 for i in ls ](visibleLists):
                if objectDict.get(objectId) is not None:
                    continue
                sphere = self._scene._objs[objectId]
                if self._players.get(objectId) is not None:
                    objectDict[objectId] = makeObjectJson(objectId, self._players[objectId].aiId, 'player', sphere.center, sphere.radius, self._players[objectId].longAttackCasting, self._players[objectId].shieldTime)
                    continue
                objType = self._objects.get(objectId).type
                objectDict[objectId] = makeObjectJson(objectId, -2, objType, sphere.center, sphere.radius)
            
            for None in enumerate(self._nutrientFlushPos):
                (i, pos) = None
                if (any,)(lambda .0: continue(visionSpheres)):
                    nutrientId = 4000000 + i
                    objectDict[nutrientId] = makeObjectJson(nutrientId, -2, 'source', pos, 0)
                    continue
        return '{"ai_id":%d,"objects":[%s]}' % (aiId, ','.join(objectDict.values()))

    
    def getStatusJson(self = None, aiId = None):
        infoList = []
        for (playerId, player) in self._players.items():
            if aiId != -1 and player.aiId != aiId:
                continue
            infoList.append(self.makePlayerJson(playerId))
        
        return '{"players":[%s]}' % ','.join(infoList)

    
    def setSpeed(self = None, playerId = None, newSpeed = None):
        speedLimit = self._players[playerId].speedLimit
        newSpeedLength = sum(lambda .0: continue(newSpeed)) ** 0.5
        if newSpeedLength > speedLimit:
            newSpeed = (None, tuple)(lambda .0: continue(newSpeed))
        self._players[playerId].speed = newSpeed

    
    def castSkill(self = None, playerId = None, skillName = None, **kw):
        if self._players[playerId].longAttackCasting >= 0:
            return None
        if None._players[playerId].skillsLV.get(skillName) is not None and self._players[playerId].skillsCD[skillName] == 0:
            if skillName == 'longAttack':
                self._castSkills[playerId] = CastLongAttackInfo(kw['player'])
            else:
                self._castSkills[playerId] = CastSkillInfo(skillName)
        

    
    def longAttackSet(self = None, playerId = None, enemyId = None):
        player = self._players.get(playerId)
        if player is None:
            raise ValueError('Player %d does not exist' % playerId)
        if self._players.get(enemyId) is None:
            raise ValueError('Enemy %d does not exist' % enemyId)
        self.healthChange(playerId, -10)
        player.skillsCD['longAttack'] = 80
        player.longAttackCasting = 10
        player.longAttackEnemy = enemyId
        self._changeList.append(self.makeSkillCastJson(playerId, 'longAttack', enemyId))

    
    def longAttackDone(self = None, playerId = None):
        player = self._players.get(playerId)
        enemyId = player.longAttackEnemy
        enemyObj = self._scene.getObject(enemyId)
        if player is None:
            raise ValueError('Player %d does not exist' % playerId)
        if player.longAttackCasting != 0:
            raise ValueError('Player %d is not completing a long attack cast' % playerId)
        skillLevel = player.skillsLV['longAttack']
        attackRange = 3000 + 500 * skillLevel
        if self._players[enemyId].shieldTime > 0 or self._players[enemyId].shieldLevel >= 5:
            player.longAttackCasting = -1
            player.longAttackEnemy = -1
            return None
        if None.dis(self._scene.getObject(playerId).center, enemyObj.center) - enemyObj.radius < attackRange:
            damage = 100 * skillLevel
            self.healthChange(enemyId, -damage)
            if skillLevel == 5:
                self._players[enemyId].stopTime = 30
            self._changeList.append(self.makeSkillHitJson('longAttack', playerId, enemyId))
        player.longAttackCasting = -1
        player.longAttackEnemy = -1

    
    def shortAttack(self = None, playerId = None):
        skillLevel = self._players[playerId].skillsLV['shortAttack']
        damage = 1000 + 200 * (skillLevel - 1)
        attackRange = 100 + 10 * (skillLevel - 1)
        self.healthChange(playerId, -50)
        self._players[playerId].skillsCD['shortAttack'] = 80
        self._changeList.append(self.makeSkillCastJson(playerId, 'shortAttack'))
        virtualSphere = scene.Sphere(self.getCenter(playerId), attackRange)
        for objId in self._scene.intersect(virtualSphere):
            if self._players.get(objId) is not None and objId != playerId and self._players[objId].shieldTime == 0 and self._players[objId].shieldLevel < 5:
                self.healthChange(objId, -damage)
                self._changeList.append(self.makeSkillHitJson('shortAttack', playerId, objId))
                continue
        if skillLevel == 5:
            self._players[playerId].shieldLevel = 35

    
    def shield(self = None, playerId = None):
        skillLevel = self._players[playerId].skillsLV['shield']
        self._players[playerId].shieldTime = 81 + 20 * skillLevel
        self._players[playerId].skillsCD['shield'] = 100
        self._changeList.append(self.makeSkillCastJson(playerId, 'shield'))

    
    def dis(self = None, pos1 = None, pos2 = None):
        return (None, sum)(lambda .0: continue(range(3))) ** 0.5

    
    def outsideMap(self = None, pos = None, radius = None):
        if pos[0] - radius < 0 and pos[0] + radius > self._mapSize and pos[1] - radius < 0 and pos[1] + radius > self._mapSize and pos[2] - radius < 0 or pos[2] + radius > self._mapSize:
            return True
        return None

    
    def dash(self = None, playerId = None):
        player = self._players.get(playerId)
        skillLevel = player.skillsLV['dash']
        if player is None:
            raise ValueError('Player %d does not exist' % playerId)
        player.dashTime = 40
        if skillLevel == 5:
            player.dashTime += 40
        player.speedLimit += skillLevel * 20
        self.healthChange(playerId, -40)
        player.skillsCD['dash'] = 100
        self._changeList.append(self.makeSkillCastJson(playerId, 'dash'))

    
    def nutrientMove(self = None, playerId = None):
        if playerId == 0:
            return None
        sphere = None._scene.getObject(playerId)
        bosssphere = self._scene.getObject(0)
        pos = (None, tuple)(lambda .0: continue(range(3)))
        while self.dis(pos, bosssphere.center) < bosssphere.radius:
            pos = (None, tuple)(lambda .0: continue(range(3)))
        newSphere = scene.Sphere(pos, sphere.radius)
        self._scene.modify(newSphere, playerId)
        self._players[playerId].nutrientMove = 2
        self._changeList.append(self.makeChangeJson(playerId, self._players[playerId].aiId, pos, newSphere.radius, 1))

    
    def visionUp(self = None, playerId = None):
        skillLevel = self._players[playerId].skillsLV['visionUp']
        self._players[playerId].vision = 5000 + 1000 * skillLevel
        self._changedPlayer.add(playerId)
        self._changeList.append(self.makeSkillCastJson(playerId, 'visionUp'))

    
    def healthUp(self = None, playerId = None):
        self.healthChange(playerId, 500)
        self._changedPlayer.add(playerId)
        self._changeList.append(self.makeSkillCastJson(playerId, 'healthUp'))

    
    def getCenter(self = None, Id = None):
        return self._scene.getObject(Id).center

    
    def upgradeSkill(self = None, playerId = None, skillName = None):
        validSkillName = [
            'shortAttack',
            'longAttack',
            'shield',
            'dash',
            'visionUp',
            'healthUp']
        if skillName not in validSkillName:
            raise ValueError('Invalid skill name')
        if self._players[playerId].skillsLV.get(skillName) is not None:
            price = self._skillPrice[skillName] * 2 ** self._players[playerId].skillsLV[skillName]
            if self._players[playerId].ability >= price and self._players[playerId].skillsLV[skillName] < 5:
                self._changedPlayer.add(playerId)
                self._players[playerId].skillsLV[skillName] += 1
                self._players[playerId].ability -= price
                if skillName == 'visionUp':
                    self.visionUp(playerId)
                if skillName == 'healthUp':
                    self.healthUp(playerId)
                
            
        else:
            price = self._skillPrice[skillName] * 2 ** len(self._players[playerId].skillsLV)
            if self._players[playerId].ability >= price:
                self._changedPlayer.add(playerId)
                self._players[playerId].skillsLV[skillName] = 1
                self._players[playerId].ability -= price
                self._players[playerId].skillsCD[skillName] = 0
                if skillName == 'visionUp':
                    self.visionUp(playerId)
                if skillName == 'healthUp':
                    self.healthUp(playerId)
                

    
    def gameEnd(self = None, winnerId = None, why = None):
        self._gameEnd = True
        self._changeList.append('{"info":"end","time":%d,"ai_id":%d,"why":%d}' % (self._time, winnerId, why))

    
    def testGameEnd(self = None, score = None):
        self._gameEnd = True
        if score > 0:
            aiId = 0
        else:
            aiId = 1
        self._changeList.append('{"info":"end","time":%d,"ai_id":%d,"score":%d}' % (self._time, aiId, score))


