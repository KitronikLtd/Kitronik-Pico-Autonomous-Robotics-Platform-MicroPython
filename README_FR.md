# Kitronik-Pico-Autonomous-Robotics-Platform-MicroPython

__Crédit:__ le fichier [README](README.md) est traduit par [MCHobby](https://shop.mchobby.be) - the [README](README.md) file is translated by [MCHobby](https://shop.mchobby.be)

Classe et code d'exemple de la plateforme robotique autonome Kitronik pour Raspberry Pi Pico. (www.kitronik.co.uk/5335)

Sur la plateforme robotique autonome:  
* Avant (_Forward_ en anglais) est définit étant à l'opposé de l'interrupteur marche/arrêt
* Gauche (_Left_) et Droite (_Right_) sont définit lorsque l'on est face à l'avant (_when facing Forward_)  
* Le Pico doit être branché avec le connecteur USB orienté à l'arrière (à l'opposé du trou prévu pour le crayon)

Pour utiliser votre buggy, sauver le fichier `PicoAutonomousRobotics.py` sur le Pico afin qu'il puisse être importé.
## Importer PicoAutonomousRobotics.py et créer une instance:
```python
    import PicoAutonomousRobotics
    robot = PicoAutonomousRobotics.KitronikPicoRobotBuggy()
 ```
Cela initialisera les broches nécessaires pour les moteurs / servos / capteurs.  
## Motors
### Contrôler un moteur:
```python
    robot.motorOn(motor, direction, speed) # moteur, direction, vitesse
```
Où:
* motor => "l" pour moteur gauche (_left_) ou "r" pour moteur droit (_right_)
* direction => "f" pour avant (_forward_) ou "r" pour arrière (_reverse_)
* speed => pour la vitesse de 0 à 100

### Arrêter un moteur:
```python
    robot.motorOff(motor) # moteur
```
Où:
* motor =>  "l" pour moteur gauche (_left_) ou "r" pour moteur droit (_right_)

## Servos
Le servo PWM est contrôlé en utilisant PIO (répétition 20ms, pour un cycle utile variant entre 500 et 2500us).  
Les sorties servos sont automatiquement préparés à l'initialisation de la classe.   
Ce processus active le générateur PWM PIO sur la broche servo.  

Si la broche doit être utilisée pour autre chose alors il est possible de libérer celle-ci en désactivant PIO ('_deregistered_').  
 ```python
    robot.deregisterServo(servo)
 ```
Pour réactiver (_re-register_) la broche servo après une désactivation:  
```python
    robot.registerServo(servo)
```
Où:
* servo => le numéro du servo-moteur (0-3)


### Piloter un servo:

```python
    robot.goToPosition(servo, degrees)
```
Où:
* servo => le numéro du servo-moteur à positionner (0-3)
* degrees => l'angle en degrés (0-180)


```python
    robot.goToPeriod(servo, period)
 ```   
Où:
* servo => le numéro du servo-moteur à positionner (0-3)
* period => période du cycle utile en micro-seconde (500-2500)

## Capteur Ultrason
### Lecture d'une distance
```python
robot.getDistance(whichSensor) # Capteur_ultrason
```
Où:
* whichSensor => "f" capteur avant (_front_') ou "r" capteur arrière (_rear_)
Le paramètre par défaut est "f", il est donc possible de faire l'appel suivant:  
```python
robot.getDistance()
```

### Fixer l'unité de mesure:  
```python
robot.setMeasurementsTo(units) # unité_a_utiliser

```
Où:
* units => "inch" pour une mesure en "Pouce" (unité impériale), "cm" pour une mesure en centimètre (système métrique)

## Suiveur de ligne
Les capteurs sont marqués sur la carte PCB pour la gauche (_left_), droite (_right_) et le centre. Le coté gauche (_Left_) est à gauche du buggy lorsqu'il est vu depuis en haut, en regardant d'en face (_facing the front_).  
Le capteur central est un peu plus en avant que les autres capteurs.

### Lires les valeurs:
```python
robot.getRawLFValue(whichSensor) # Quel_capteur
```
Résultat:
* la valeur brute du capteur entre 0 et 65535 (faible valeur numérique représente une surface sombre)  

Où:
* whichSensor => Indique le capteur interrogé: "c" pour centre, "l" pour gauche (_left_), "r" pour droite (_right_)

Les capteurs du suiveur de ligne peuvent aussi retourner une valeur booléenne **True** ou **False**:
```python
robot.isLFSensorLight(whichSensor) # Quel_capteur
```
Résultat:  
* **True** lorsque le capteur est au dessus d'une surface claire et **False** lorsqu'il est au dessus d'une surface sombre.

Où:
* whichSensor => Indique le capteur interrogé: "c" pour centre, "l" pour gauche (_left_), "r" pour droite (_right_)

### Fixer les seuil clair / sombre:
La détermination surface claire / sombre est basée sur les seuils "darkThreshold" (sombre) et "lightThreshold" (clair).  
Utilisez le code suivant pour modifier les seuils:
```python
robot.setLFDarkValue(darkThreshold, OptionalLeftThreshold = -1, OptionalRightThreshold = -1) # Seuil_sombre, Seuil_gauche_optionnel, Seuil_droit_optionnel
```
```python
robot.setLFLightValue(lightThreshold, OptionalLeftThreshold = -1, OptionalRightThreshold = -1) # Seuil_clair, Seuil_gauche_optionnel, Seuil_droit_optionnel
```
Les valeurs typique pour des surfaces claires (_light_) son en dessous de 20000 et au dessus de 30000 pour une surface sombre (_dark_).  
Les seuils optionnels permettent d'avoir des valeurs différentes pour les capteurs de gauche et de droite, dans ce cas, la première valeur correspond au seuil du capteur central.  
Si les valeurs optionnelles ne sont pas utilisées alors les 3 capteurs utilisent les mêmes valeur de seuils.


## Buzzer
Le buzzer est piloté par un signal PWM.  

### Produire un son:  
```python
robot.soundFrequency(frequency) # Frequence
```
Où:
  * frequency => la fréquence du son à produire entre 0 et 3000 Hertz

### Désactiver le buzzer:
```python
robot.silence()
```

### Beeper (comme un klaxon de voiture):
```python        
robot.beepHorn():
```

## LEDs ZIP
Les LEDs ZIP ont un fonctionnement en deux étapes...
### Initialiser les LEDs ZIP:  
Indiquer la couleur attribuée aux différentes LEDs:  
```python
robot.setLED(whichLED, whichColour) # Quelle_LED, Quelle_couleur
```
Où:  
* whichLED => indique la LED concernée (0-3)  
* whichColour => indique la couleur assignée à la LED soit à l'aide d'un tuple `(valeur_rouge, valeur_vert, valeur_bleu)` ou à l'aide d'une des constantes prédéfinies:
```python
# BLACK=Noir, RED=Rouge, YELLOW=Jaune, GREEN=Vert, CYAN=Cyan,
# BLUE=Bleu, PURPLE=Pourpre, WHITE=Blanc
COLOURS = (BLACK, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)
```

Eteindre les LEDs:
```python
robot.clear(whichLED) # Quelle_LED
```
Où:  
* whichLED => indique la LED à éteindre (0-3)

Contrôler le luminosité:
```python
robot.setBrightness(value)
```
Où:  
* value => Luminosité de toutes les LEDs entre 0 et 100 (luminosité en %)

### Appliquer les changements:
```python
robot.show()
```

# Dépannage

Ce code est conçu pour être utilisé comme un module. Voir: https://kitronik.co.uk/blogs/resources/modules-micro-python-and-the-raspberry-pi-pico (_anglais_) pour plus d'information.
