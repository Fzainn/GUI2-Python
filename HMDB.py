# 1 - remove the header from the metabolites_file
# 2- replace any "," to "-" in names of metabolites in metabolites_file

import os
import re


def is_number(x):
    try:
        float(x)
        return(True)
    except:
        return(False)

metabolites_file = r"metabolites-2022-03-09-edit.csv" #input 1
peaks_folder = r"D:\Ali\HMDB DBs 2022\9-2022\hmdb_experimental_msms_peak_lists" #input2

msp_file = r"HMDB_endogenous_EXP_pos.msp" #output folder

MODE = "Positive" #input
adduct =  +1.007276 #input


with open(metabolites_file, "r",  encoding="utf8") as info:
    info = info.readlines()


count = 0

print(">>>>>LOADING<<<<<")
for i_info in info:
    
    count = count + 1
    i_info = i_info.split(",")
    idss = i_info[0]
    name = i_info[1]
    formula = i_info[4]
    mw =  i_info[5]
    precursoeMZ = i_info[6]

    peaks_files = [f for f in os.listdir(peaks_folder) if idss in f]
 
    
    for i_peaks in peaks_files:
        peaks_list_all = []
        with open(f"{peaks_folder}\\{i_peaks}", "r") as peaks:
            peaks = peaks.readlines()
        
        for j_peaks in peaks:
            
            j_peaks = j_peaks.replace("\n", "")
            j_peaks = j_peaks.split("\t")


            if len(j_peaks) == 1:
                j_peaks = j_peaks[0]
                j_peaks = j_peaks.split(" ")


            if len(j_peaks) > 2:
                j_peaks = j_peaks[1:3]


            if len(j_peaks) == 2:
                mzmz = j_peaks[0].strip().split(" ")

                if is_number(mzmz[0]):
                    if len(mzmz) == 2:
                        j_peaks = [mzmz[0], mzmz[1]]
                    else:
                        intint = j_peaks[1].strip()
                        intint = intint.split(" ")
                        intint= intint[0]
                        j_peaks = [j_peaks[0],intint]

            if is_number(j_peaks[0].strip())  and len(j_peaks) != 1:
                if is_number(j_peaks[1].strip()):
                    j_peaks = [float(i.strip()) for i in j_peaks]
                    
                    j_peaks_mz = j_peaks[0]

                    j_peaks_int = j_peaks[1]

                    p_list = [str(j_peaks_mz), str(j_peaks_int)]

                    peaks_list_all.append("\t".join(p_list))

        
        try:
            precursoeMZ = float(precursoeMZ) + (adduct)
        except:
            pass
        with open(f"{msp_file}", "a") as msp:
            msp.write(f"NAME: {idss}\nDB#: HMDB\nSpectrum_type: MS2\nIONMODE: {MODE}\nFORMULA: {formula}\nMW: {mw}\nPRECURSORMZ: {precursoeMZ}\n")



        with open(f"{msp_file}", "a") as msp:
            msp.write(f"Num Peaks: {len(peaks_list_all)}\n")


        for z_peak in peaks_list_all:

            
            with open(f"{msp_file}", "a") as msp:
                msp.write(f"{z_peak}\n")

        with open(f"{msp_file}", "a") as msp:
            msp.write(f"\n\n")

print(">>>DONE>>>>>>DONE>>>>>>>DONE>>>>>>DONE<<<<<<<<<<DONE<<<<<<DONE<<<<")





    
