#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interactive

# Gum constants:
# Surface area of gum
Surface_Area_of_Gum_int = 1
# Gum saliva mass transfer coefficient
hsf_int = 0.5
# Gum saliva partition coefficient
Ksf_int = 0.5
# Saliva gas partition coefficient
Kgs_int = 0.005

# Initial conditions:
# Mass of flavor in gum
Mass_of_Flavor_in_Gum_int = 90
# Mass of flavor in saliva
Mass_of_Flavor_in_Saliva_int = 0
# Mass of flavor in gas
Mass_of_Flavor_in_Gas_int = 0
# Volume of gum
Volume_of_Gum_int = 1
# Volume of saliva
Volume_of_Saliva_int = 1.2
# volume of gas
Volume_of_Gas_int = 5

# Time factors:
# Time step
Timestep_int = 0.1
# 1/timestep
tsf = 1 / Timestep_int

# Swallowing factors:
# Saliva production rate
Salrate_int = 2 / 60
# Swallowing rate
Swallowtime_int = 10

# Breathing factors:
# Time between breaths
Time_Between_Breath_int = 2
# Fraction of flavoring left in the nasal cavity after a breath
Flavor_Left_After_Breath_int = 0

# Lists and arrays:
t = np.arange(0, 100, Timestep_int)
tdiff = np.arange(0, 1000, Timestep_int)


def MassPlot(Mfgum=Mass_of_Flavor_in_Gum_int, SArea=Surface_Area_of_Gum_int, hsf=hsf_int,
             Ksf=Ksf_int, Vgum=Volume_of_Gum_int, Mfs=Mass_of_Flavor_in_Saliva_int,
             Vsaliva=Volume_of_Saliva_int, Kgs=Kgs_int, Vgas=Volume_of_Gas_int,
             Mfgas=Mass_of_Flavor_in_Gas_int, Fbreath=Flavor_Left_After_Breath_int,
             Swallowtime=Swallowtime_int, BreathInt=Time_Between_Breath_int, Salrate=Salrate_int):
    MassInGum = []
    MassInGas = []
    MassInSaliva = []
    dmdt = []
    for i in range(0, len(t)):
        MassInGum.append(Mfgum)
        MassInGas.append(Mfgas)
        MassInSaliva.append(Mfs)
        delmsf = (Timestep_int * SArea * hsf * (Ksf * (Mfgum / Vgum) - (Mfs / Vsaliva)))
        dmdt.append(delmsf * tsf)
        Mfgas = (Kgs * (Mfs / Vsaliva) * Vgas)
        delmgs = Mfgas - MassInGas[i - 1]
        Mfgum -= delmsf
        Mfs += delmsf - delmgs
        Vsaliva += Salrate * Timestep_int
        if t[i] % Swallowtime == 0:
            vsprime = Vsaliva
            Vsaliva = 0.85
            Mfs *= Vsaliva / vsprime
        if t[i] % BreathInt == 0:
            Mfgas *= Fbreath
    fig = plt.figure(figsize=(12, 8))
    plt.plot(t, MassInGum, label='Mass in Gum')
    plt.plot(t, MassInSaliva, label='Mass in Saliva')
    plt.plot(t, MassInGas, label='Mass in Gas')
    plt.xlabel('Time (s)')
    plt.ylabel('Mass (mg)')
    plt.title('Flavor Mass in Gum, Saliva and Gas Phase')
    plt.legend()


def TransferPlot(Mfgum=Mass_of_Flavor_in_Gum_int, SArea=Surface_Area_of_Gum_int, hsf=hsf_int,
                 Ksf=Ksf_int, Vgum=Volume_of_Gum_int, Mfs=Mass_of_Flavor_in_Saliva_int,
                 Vsaliva=Volume_of_Saliva_int, Kgs=Kgs_int, Vgas=Volume_of_Gas_int,
                 Mfgas=Mass_of_Flavor_in_Gas_int, Fbreath=Flavor_Left_After_Breath_int,
                 Swallowtime=Swallowtime_int, BreathInt=Time_Between_Breath_int, Salrate=Salrate_int):
    MassInGum = []
    MassInGas = []
    MassInSaliva = []
    dmdt = []
    for i in range(0, len(t)):
        MassInGum.append(Mfgum)
        MassInGas.append(Mfgas)
        MassInSaliva.append(Mfs)
        delmsf = (Timestep_int * SArea * hsf * (Ksf * (Mfgum / Vgum) - (Mfs / Vsaliva)))
        dmdt.append(delmsf * tsf)
        Mfgas = (Kgs * (Mfs / Vsaliva) * Vgas)
        delmgs = Mfgas - MassInGas[i - 1]
        Mfgum -= delmsf
        Mfs += delmsf - delmgs
        Vsaliva += Salrate * Timestep_int
        if t[i] % Swallowtime == 0:
            vsprime = Vsaliva
            Vs = 0.85
            Mfs *= Vsaliva / vsprime
        if t[i] % BreathInt == 0:
            Mfgas *= Fbreath
    fig = plt.figure(figsize=(12, 8))
    plt.plot(t, dmdt)
    plt.xlabel('Time (s)')
    plt.ylabel('Flavor Release Rate (mg/ms)')
    plt.title('Flavor Release')


def RelativeConc(Mfgum=Mass_of_Flavor_in_Gum_int, SArea=Surface_Area_of_Gum_int, hsf=hsf_int,
                 Ksf=Ksf_int, Vgum=Volume_of_Gum_int, Mfs=Mass_of_Flavor_in_Saliva_int,
                 Vsaliva=Volume_of_Saliva_int, Kgs=Kgs_int, Vgas=Volume_of_Gas_int,
                 Mfgas=Mass_of_Flavor_in_Gas_int, Fbreath=Flavor_Left_After_Breath_int,
                 Swallowtime=Swallowtime_int, BreathInt=Time_Between_Breath_int, Salrate=Salrate_int):
    MassInGum = []
    MassInGas = []
    MassInSaliva = []
    dmdt = []
    RelConcG = []
    for i in range(0, len(tdiff)):
        MassInGum.append(Mfgum)
        MassInGas.append(Mfgas)
        MassInSaliva.append(Mfs)
        delmsf = (Timestep_int * SArea * hsf * (Ksf * (Mfgum / Vgum) - (Mfs / Vsaliva)))
        dmdt.append(delmsf * tsf)
        Mfgas = (Kgs * (Mfs / Vsaliva) * Vgas)
        delmgs = Mfgas - MassInGas[i - 1]
        Mfgum -= delmsf
        Mfs += delmsf - delmgs
        Vsaliva += Salrate * Timestep_int
        if tdiff[i] % Swallowtime == 0:
            vsprime = Vsaliva
            Vs = 0.85
            Mfs *= Vsaliva / vsprime
        if tdiff[i] % BreathInt == 0:
            Mfgas *= Fbreath
        RelConcG.append((Mfgum / Vgum) / (MassInGum[0] / Vgum))
    fig = plt.figure(figsize=(12, 8))
    plt.plot(tdiff, RelConcG)
    plt.xlabel('Time (s)')
    plt.ylabel('Relative Concentration')
    plt.title('Relative Concentrations')


def RelativeConcGS(Mfgum=Mass_of_Flavor_in_Gum_int, SArea=Surface_Area_of_Gum_int, hsf=hsf_int,
                   Ksf=Ksf_int, Vgum=Volume_of_Gum_int, Mfs=Mass_of_Flavor_in_Saliva_int,
                   Vsaliva=Volume_of_Saliva_int, Kgs=Kgs_int, Vgas=Volume_of_Gas_int,
                   Mfgas=Mass_of_Flavor_in_Gas_int, Fbreath=Flavor_Left_After_Breath_int,
                   Swallowtime=Swallowtime_int, BreathInt=Time_Between_Breath_int, Salrate=Salrate_int):
    MassInGum = []
    MassInGas = []
    MassInSaliva = []
    dmdt = []
    RelConcGS = []
    for i in range(0, len(tdiff)):
        MassInGum.append(Mfgum)
        MassInGas.append(Mfgas)
        MassInSaliva.append(Mfs)
        delmsf = (Timestep_int * SArea * hsf * (Ksf * (Mfgum / Vgum) - (Mfs / Vsaliva)))
        dmdt.append(delmsf * tsf)
        Mfgas = (Kgs * (Mfs / Vsaliva) * Vgas)
        delmgs = Mfgas - MassInGas[i - 1]
        Mfgum -= delmsf
        Mfs += delmsf - delmgs
        Vsaliva += Salrate * Timestep_int
        if tdiff[i] % Swallowtime == 0:
            vsprime = Vsaliva
            Vs = 0.85
            Mfs *= Vsaliva / vsprime
        if tdiff[i] % BreathInt == 0:
            Mfgas *= Fbreath
        RelConcGS.append((Mfs / Vsaliva) / (MassInGum[i] / Vgum))
    fig = plt.figure(figsize=(12, 8))
    plt.plot(tdiff, RelConcGS)
    plt.xlabel('Time (s)')
    plt.ylabel('Relative Concentration')
    plt.title('Relative Concentrations')


def ConcFlavor(Mfgum=Mass_of_Flavor_in_Gum_int, SArea=Surface_Area_of_Gum_int, hsf=hsf_int,
               Ksf=Ksf_int, Vgum=Volume_of_Gum_int, Mfs=Mass_of_Flavor_in_Saliva_int,
               Vsaliva=Volume_of_Saliva_int, Kgs=Kgs_int, Vgas=Volume_of_Gas_int,
               Mfgas=Mass_of_Flavor_in_Gas_int, Fbreath=Flavor_Left_After_Breath_int,
               Swallowtime=Swallowtime_int, BreathInt=Time_Between_Breath_int, Salrate=Salrate_int):
    MassInGum = []
    MassInGas = []
    MassInSaliva = []
    dmdt = []
    ConcFlavor = []
    for i in range(0, len(tdiff)):
        MassInGum.append(Mfgum)
        MassInGas.append(Mfgas)
        MassInSaliva.append(Mfs)
        delmsf = (Timestep_int * SArea * hsf * (Ksf * (Mfgum / Vgum) - (Mfs / Vsaliva)))
        dmdt.append(delmsf * tsf)
        Mfgas = (Kgs * (Mfs / Vsaliva) * Vgas)
        delmgs = Mfgas - MassInGas[i - 1]
        Mfgum -= delmsf
        Mfs += delmsf - delmgs
        Vsaliva += Salrate * Timestep_int
        if tdiff[i] % Swallowtime == 0:
            vsprime = Vsaliva
            Vs = 0.85
            Mfs *= Vsaliva / vsprime
        if tdiff[i] % BreathInt == 0:
            Mfgas *= Fbreath
        ConcFlavor.append((Mfs / Vsaliva))
    fig = plt.figure(figsize=(12, 8))
    plt.plot(tdiff, ConcFlavor)
    plt.xlabel('Time (s)')
    plt.ylabel('Concentration')
    plt.title('Concentration of Flavor in Saliva')


# In[5]:


MassPlot(Mass_of_Flavor_in_Gum_int, Surface_Area_of_Gum_int, hsf_int, Ksf_int, Volume_of_Gum_int,
         Mass_of_Flavor_in_Saliva_int, Volume_of_Saliva_int, Kgs_int, Volume_of_Gas_int,
         Mass_of_Flavor_in_Gas_int, Flavor_Left_After_Breath_int, Swallowtime_int,
         Time_Between_Breath_int, Salrate_int)


interactive_plot = interactive(MassPlot, Mfgum=(0, 180), SArea=(0, 10), hsf=(0.1, 100),
                               Ksf=(0.1, 100), Vgum=(0.1, 1), Mfs=(0, 0.5), Vsaliva=(1, 5, 0.2),
                               Kgs=(0.001, 0.1, 0.001), Vgas=(0.1, 10), Mfgas=(0, 1), FBreath=(0, 1, 0.1),
                               Swallowtime=(1, 1000), BreathInt=(1, 1000), Salrate=(0, 0.12, 0.01))

interactive_plot

interactive_plot = interactive(TransferPlot, Mfgum=(0, 180), SArea=(0, 10), hsf=(0.1, 10),
                               Ksf=(0.1, 100), Vgum=(0.1, 1), Mfs=(0, 0.5), Vsaliva=(1, 5, 0.2),
                               Kgs=(0.1, 100), Vgas=(0.1, 10), Mfgas=(0, 1), FBreath=(0, 1, 0.1),
                               Swallowtime=(1, 10), BreathInt=(1, 5), Salrate=(0, 0.12, 0.01))
# output = interactive_plot.children[-1]
interactive_plot

# In[8]:


RelativeConc(Mass_of_Flavor_in_Gum_int, Surface_Area_of_Gum_int, hsf_int, Ksf_int, Volume_of_Gum_int,
             Mass_of_Flavor_in_Saliva_int, Volume_of_Saliva_int, Kgs_int, Volume_of_Gas_int,
             Mass_of_Flavor_in_Gas_int, Flavor_Left_After_Breath_int, Swallowtime_int,
             Time_Between_Breath_int, Salrate_int)

# In[9]:


interactive_plot = interactive(RelativeConc, Mfgum=(0, 180), SArea=(0, 10), hsf=(0.1, 10),
                               Ksf=(0.05, 100), Vgum=(0.1, 1), Mfs=(0, 0.5), Vsaliva=(1, 5, 0.2),
                               Kgs=(0.1, 100), Vgas=(0.1, 10), Mfgas=(0, 1), FBreath=(0, 1, 0.1),
                               Swallowtime=(1, 10), BreathInt=(1, 5), Salrate=(0, 0.12, 0.01))
interactive_plot

# In[10]:


RelativeConcGS(Mass_of_Flavor_in_Gum_int, Surface_Area_of_Gum_int, hsf_int, Ksf_int, Volume_of_Gum_int,
               Mass_of_Flavor_in_Saliva_int, Volume_of_Saliva_int, Kgs_int, Volume_of_Gas_int,
               Mass_of_Flavor_in_Gas_int, Flavor_Left_After_Breath_int, Swallowtime_int,
               Time_Between_Breath_int, Salrate_int)

# In[11]:


interactive_plot = interactive(RelativeConcGS, Mfgum=(0, 180), SArea=(0, 10), hsf=(0.1, 10),
                               Ksf=(0.05, 100), Vgum=(0.1, 1), Mfs=(0, 0.5), Vsaliva=(1, 5, 0.2),
                               Kgs=(0.005, 0.1), Vgas=(0.1, 10), Mfgas=(0, 1), FBreath=(0, 1, 0.1),
                               Swallowtime=(1, 10), BreathInt=(1, 5), Salrate=(0, 0.12, 0.01))
interactive_plot

# In[12]:


interactive_plot = interactive(ConcFlavor, Mfgum=(0, 180), SArea=(0, 10), hsf=(0.1, 10),
                               Ksf=(0.05, 100), Vgum=(0.1, 1), Mfs=(0, 0.5), Vsaliva=(1, 5, 0.2),
                               Kgs=(0.005, 100), Vgas=(0.1, 10), Mfgas=(0, 1), FBreath=(0, 1, 0.1),
                               Swallowtime=(1, 10), BreathInt=(1, 5), Salrate=(0, 0.12, 0.01))
interactive_plot
