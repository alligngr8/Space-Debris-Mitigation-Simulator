import operator
import orbitalRemovalMethod as removal
import dataProcessing
import riskEvaluation as risk
import cost


def costSensitivity():
    costIter = iter([10000000, 100000000, 290000000/2, 290000000, 290000000*2, 1000000000])
    # Base ROI Lists
    ROIlistIBS = []
    ROIlistPropellant = []
    ROIlistEDT = []
    ROIlistEDDE = []
    for baseCost in costIter:
        # Method Definitons
        IBS = removal.orbitalRemovalMethod("IBS", (3000, 5000), (300, 1000), 1.71, baseCost + 0.06896551724*baseCost)
        robotArmPropellant = removal.orbitalRemovalMethod("Robot Arm -- Propellant", (65, 3800), (750, 900), 5, baseCost + 0.03448275862*baseCost)
        robotArmEDT = removal.orbitalRemovalMethod("Robot Arm -- EDT", (500, 3400), (800, 1400), 1, baseCost)
        EDDE = removal.orbitalRemovalMethod("EDDE", (2, 50), (800, 1000), 357, baseCost - 0.1034482759*baseCost)
        # Data Processing
        orbitalObjects = dataProcessing.junkList("spaceobjects.csv")

        # Sort List
        orbitalObjects.sort(key=operator.attrgetter('weightedRisk'))
        orbitalObjects = risk.normalizeWeightedRisk(orbitalObjects)
        orbitalObjects.reverse()

        years = 5
        IBSresults = removal.debrisRemoval(IBS, orbitalObjects, years)
        Propellantresults = removal.debrisRemoval(robotArmPropellant, orbitalObjects, years)
        EDTresults = removal.debrisRemoval(robotArmEDT, orbitalObjects, years)
        EDDEresults = removal.debrisRemoval(EDDE, orbitalObjects, years)

        ROIlistIBS.append(cost.ROI(IBSresults, IBS))
        ROIlistPropellant.append(cost.ROI(Propellantresults, robotArmPropellant))
        ROIlistEDT.append(cost.ROI(EDTresults, robotArmEDT))
        ROIlistEDDE.append(cost.ROI(EDDEresults, EDDE))

    print ROIlistIBS
    print ROIlistPropellant
    print ROIlistEDT
    print ROIlistEDDE

    # ROIaverageIBS = np.mean(ROIlistIBS)
    # ROIaveragePropellant = np.mean(ROIlistPropellant)
    # ROIaverageEDT = np.mean(ROIlistEDT)
    # ROIaverageEDDE = np.mean(ROIlistEDDE)

    # MissionRiskIBS = np.mean(MissionRisklistIBS)
    # MissionRiskPropellant = np.mean(MissionRisklistPropellant)
    # MissionRiskEDT = np.mean(MissionRisklistEDT)
    # MissionRiskEDDE = np.mean(MissionRisklistEDDE)

    # print "ROI Average IBS:         " + str(ROIaverageIBS) + " Mission Risk: " + str(MissionRiskIBS)
    # print "ROI Average Propellant:  " + str(ROIaveragePropellant) + " Mission Risk: " + str(MissionRiskPropellant)
    # print "ROI Average EDT:         " + str(ROIaverageEDT) + " Mission Risk: " + str(MissionRiskEDT)
    # print "ROI Average EDDE:        " + str(ROIaverageEDDE) + " Mission Risk: " + str(MissionRiskEDDE)


def probabilitySensitivity():
    baseCost = 290000000
    # Method Definitons
    IBS = removal.orbitalRemovalMethod("IBS", (3000, 5000), (300, 1000), 1.71, baseCost + 20000000)
    robotArmPropellant = removal.orbitalRemovalMethod("Robot Arm -- Propellant", (65, 3800), (750, 900), 5, baseCost + 10000000)
    robotArmEDT = removal.orbitalRemovalMethod("Robot Arm -- EDT", (500, 3400), (800, 1400), 1, baseCost)
    EDDE = removal.orbitalRemovalMethod("EDDE", (2, 50), (800, 1000), 357, baseCost - 30000000)
    # Data Processing
    orbitalObjects = dataProcessing.junkList("spaceobjects.csv")

    # Base ROI Lists
    ROIlistIBS = []
    ROIlistPropellant = []
    ROIlistEDT = []
    ROIlistEDDE = []

    # Sort List
    orbitalObjects.sort(key=operator.attrgetter('weightedRisk'))
    orbitalObjects = risk.normalizeWeightedRisk(orbitalObjects)
    orbitalObjects.reverse()

    crashIter = iter([1/2., 1/5., 1/50., 1/100., 1/221., 1/400.])

    for crash in crashIter:
        years = 5
        IBSresults = removal.debrisRemoval(IBS, orbitalObjects, years)
        Propellantresults = removal.debrisRemoval(robotArmPropellant, orbitalObjects, years)
        EDTresults = removal.debrisRemoval(robotArmEDT, orbitalObjects, years)
        EDDEresults = removal.debrisRemoval(EDDE, orbitalObjects, years)

        ROIlistIBS.append(cost.ROI(IBSresults, IBS, probabilityOfCrash=crash))
        ROIlistPropellant.append(cost.ROI(Propellantresults, robotArmPropellant, probabilityOfCrash=crash))
        ROIlistEDT.append(cost.ROI(EDTresults, robotArmEDT, probabilityOfCrash=crash))
        ROIlistEDDE.append(cost.ROI(EDDEresults, EDDE, probabilityOfCrash=crash))

    print ROIlistIBS
    print ROIlistPropellant
    print ROIlistEDT
    print ROIlistEDDE


def tier2Averaged():
    baseCost = 290000000
    # Method Definitons
    IBS = removal.orbitalRemovalMethod("IBS", (3000, 5000), (300, 1000), 1.71, baseCost + 20000000)
    robotArmPropellant = removal.orbitalRemovalMethod("Robot Arm -- Propellant", (65, 3800), (750, 900), 5, baseCost + 10000000)
    robotArmEDT = removal.orbitalRemovalMethod("Robot Arm -- EDT", (500, 3400), (800, 1400), 1, baseCost)
    EDDE = removal.orbitalRemovalMethod("EDDE", (2, 50), (800, 1000), 357, baseCost - 30000000)
    # Data Processing
    orbitalObjects = dataProcessing.junkList("spaceobjects.csv")

    # Base ROI Lists
    ROIlistIBS = []
    ROIlistPropellant = []
    ROIlistEDT = []
    ROIlistEDDE = []

    MissionRisklistIBS = []
    MissionRisklistPropellant = []
    MissionRisklistEDT = []
    MissionRisklistEDDE = []

    # Sort List
    orbitalObjects.sort(key=operator.attrgetter('weightedRisk'))
    orbitalObjects = risk.normalizeWeightedRisk(orbitalObjects)
    orbitalObjects.reverse()

    for i in range(0, 1000):
        years = 5
        IBSresults = removal.debrisRemoval(IBS, orbitalObjects, years)
        Propellantresults = removal.debrisRemoval(robotArmPropellant, orbitalObjects, years)
        EDTresults = removal.debrisRemoval(robotArmEDT, orbitalObjects, years)
        EDDEresults = removal.debrisRemoval(EDDE, orbitalObjects, years)

        ROIlistIBS.append(cost.ROI(IBSresults, IBS))
        ROIlistPropellant.append(cost.ROI(Propellantresults, robotArmPropellant))
        ROIlistEDT.append(cost.ROI(EDTresults, robotArmEDT))
        ROIlistEDDE.append(cost.ROI(EDDEresults, EDDE))

        MissionRisklistIBS.append(risk.missionRisk(IBSresults))
        MissionRisklistPropellant.append(risk.missionRisk(Propellantresults))
        MissionRisklistEDT.append(risk.missionRisk(EDTresults))
        MissionRisklistEDDE.append(risk.missionRisk(EDDEresults))
    import numpy as np
    ROIaverageIBS = np.mean(ROIlistIBS)
    ROIaveragePropellant = np.mean(ROIlistPropellant)
    ROIaverageEDT = np.mean(ROIlistEDT)
    ROIaverageEDDE = np.mean(ROIlistEDDE)

    MissionRiskIBS = np.mean(MissionRisklistIBS)
    MissionRiskPropellant = np.mean(MissionRisklistPropellant)
    MissionRiskEDT = np.mean(MissionRisklistEDT)
    MissionRiskEDDE = np.mean(MissionRisklistEDDE)

    print "ROI Average IBS:         " + str(ROIaverageIBS) + " Mission Risk: " + str(MissionRiskIBS)
    print "ROI Average Propellant:  " + str(ROIaveragePropellant) + " Mission Risk: " + str(MissionRiskPropellant)
    print "ROI Average EDT:         " + str(ROIaverageEDT) + " Mission Risk: " + str(MissionRiskEDT)
    print "ROI Average EDDE:        " + str(ROIaverageEDDE) + " Mission Risk: " + str(MissionRiskEDDE)


def tier3():
    baseCost = 290000000
    IBS = removal.orbitalRemovalMethod("IBS", (3000, 5000), (300, 1000), 1.71, baseCost + 20000000)
    robotArmPropellant = removal.orbitalRemovalMethod("Robot Arm -- Propellant", (65, 3800), (750, 900), 5, baseCost + 10000000)
    robotArmEDT = removal.orbitalRemovalMethod("Robot Arm -- EDT", (500, 3400), (800, 1400), 1, baseCost)
    EDDE = removal.orbitalRemovalMethod("EDDE", (2, 50), (800, 1000), 357, baseCost - 30000000)
    orbitalObjects = dataProcessing.junkList("spaceobjects.csv")
    # Base ROI Lists
    ROIlistIBS = []
    ROIlistPropellant = []
    ROIlistEDT = []
    ROIlistEDDE = []

    # Combination ROI Lists
    ROIlistIBS_Propellant = []
    ROIlistIBS_EDT = []
    ROIlistIBS_EDDE = []
    ROIlistPropellant_EDT = []
    ROIlistPropellant_EDDE = []
    ROIlistEDT_EDDE = []

    MissionRisklistIBS = []
    MissionRisklistPropellant = []
    MissionRisklistEDT = []
    MissionRisklistEDDE = []

    MissionRisklistIBS_Propellant = []
    MissionRisklistIBS_EDT = []
    MissionRisklistIBS_EDDE = []
    MissionRisklistPropellant_EDT = []
    MissionRisklistPropellant_EDDE = []
    MissionRisklistEDT_EDDE = []

    for i in range(0, 1):
        # Sort List
        orbitalObjects.sort(key=operator.attrgetter('weightedRisk'))
        orbitalObjects = risk.normalizeWeightedRisk(orbitalObjects)
        orbitalObjects.reverse()
        # Risk Analysis
        for years in range(0, 200):
            IBSresults = removal.debrisRemoval(IBS, orbitalObjects, years)
            Propellantresults = removal.debrisRemoval(robotArmPropellant, orbitalObjects, years)
            EDTresults = removal.debrisRemoval(robotArmEDT, orbitalObjects, years)
            EDDEresults = removal.debrisRemoval(EDDE, orbitalObjects, years)

            IBS_Propellanresults = removal.debrisRemoval(robotArmPropellant, IBSresults, years)
            IBS_EDTresults = removal.debrisRemoval(robotArmEDT, IBSresults, years)
            IBS_EDDEresults = removal.debrisRemoval(EDDE, IBSresults, years)
            Propellant_EDTresults = removal.debrisRemoval(robotArmEDT, Propellantresults, years)
            Propellant_EDDEresults = removal.debrisRemoval(EDDE, Propellantresults, years)
            EDT_EDDEresults = removal.debrisRemoval(EDDE, EDTresults, years)

            ROIlistIBS.append(cost.ROI(IBSresults, IBS))
            ROIlistPropellant.append(cost.ROI(Propellantresults, robotArmPropellant))
            ROIlistEDT.append(cost.ROI(EDTresults, robotArmEDT))
            ROIlistEDDE.append(cost.ROI(EDDEresults, EDDE))

            ROIlistIBS_Propellant.append(cost.ROI(IBS_Propellanresults, IBS, robotArmPropellant))
            ROIlistIBS_EDT.append(cost.ROI(IBS_EDTresults, IBS, robotArmEDT))
            ROIlistIBS_EDDE.append(cost.ROI(IBS_EDDEresults, IBS, EDDE))
            ROIlistPropellant_EDT.append(cost.ROI(Propellant_EDTresults, robotArmPropellant, robotArmEDT))
            ROIlistPropellant_EDDE.append(cost.ROI(Propellant_EDDEresults, robotArmPropellant, EDDE))
            ROIlistEDT_EDDE.append(cost.ROI(EDT_EDDEresults, robotArmEDT, EDDE))

            MissionRisklistIBS.append(risk.missionRisk(IBSresults))
            MissionRisklistPropellant.append(risk.missionRisk(Propellantresults))
            MissionRisklistEDT.append(risk.missionRisk(EDTresults))
            MissionRisklistEDDE.append(risk.missionRisk(EDDEresults))

            MissionRisklistIBS_Propellant.append(risk.missionRisk(IBS_Propellanresults))
            MissionRisklistIBS_EDT.append(risk.missionRisk(IBS_EDTresults))
            MissionRisklistIBS_EDDE.append(risk.missionRisk(IBS_EDDEresults))
            MissionRisklistPropellant_EDT.append(risk.missionRisk(Propellant_EDTresults))
            MissionRisklistPropellant_EDDE.append(risk.missionRisk(Propellant_EDDEresults))
            MissionRisklistEDT_EDDE.append(risk.missionRisk(EDT_EDDEresults))

        for debris in orbitalObjects:
            debris.scramble()
    print ROIlistIBS
    print ROIlistPropellant
    print ROIlistEDT
    print ROIlistEDDE
    print ROIlistIBS_Propellant
    print ROIlistIBS_EDT
    print ROIlistIBS_EDDE
    print ROIlistPropellant_EDT
    print ROIlistPropellant_EDDE
    print ROIlistEDT_EDDE
    print MissionRisklistIBS
    print MissionRisklistPropellant
    print MissionRisklistEDT
    print MissionRisklistEDDE
    print MissionRisklistIBS_Propellant
    print MissionRisklistIBS_EDT
    print MissionRisklistIBS_EDDE
    print MissionRisklistPropellant_EDT
    print MissionRisklistPropellant_EDDE
    print MissionRisklistEDT_EDDE
