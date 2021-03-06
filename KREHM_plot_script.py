import matplotlib
import numpy as np

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

from matplotlib import cm
import os
import cmath
import re
import resource

from scipy import special


#plt.ioff()

r = re.compile(r'(?<=\d)\-(?=\d)')

time_re = re.compile(r'\d+\.\d+')

re_f_float_neg = re.compile('(-?[0-9.]*)(-\d\d\d)')



def Gamma0(x):

    if x>150 or x == 0:

        return 0

    else: 

        return special.iv(0, x)*np.exp(-x)



#summary of functions available in this script with their description 

#a more detailed description is available for each function just below its declaration

#Getresolution -> this is a subroutine used to obtain information such as lx, ly, nlx, npe etc. from a viriato .in file

#xy -> creates a series of contour plots of density and apar field perturpations - the xy plane is plotted at different z locations

#cuts -> creates contour plots of density and apar at different location 

#all_cuts -> basically it iterates the cuts function over all of the fields files

#spectra -> plots energy spectra; can take one or more files as input (if more the one the purpose is for comparison)

#invariants -> plots time traces from invariants.dat file - one or more files can be given as input - if it's more than one then it's for comparison



def GetResolution(filenm):

    #this function is used to obtain the necessary parameters from the Viriato input file

    if 'energyk' in filenm:

        filenmroot = filenm.split('_energy')[0]

    else: 

        filenmroot = filenm.split('_fields')[0]

    filename = filenmroot + '.in'

    inputfile = open(filename,'r')

    lines = inputfile.readlines()

    lxline = lyline = lzline = nlxline = nlyline = nlzline = ngtotline = npeline = npezline = rhoiline = rhosline = deline = hyper_orderline = hyper_order_gline = hyper_morderline = 0

    for i in lines:

        if i.find('nlx')!=-1:

            nlxline = i

        if i.find('nly')!=-1:

            nlyline = i

        if i.find('nlz')!=-1:

            nlzline = i

        if i.find('npe ')!=-1:

            npeline = i

        if i.find('npez')!=-1:

            npezline = i

        if i.find('ngtot')!=-1:

            ngtotline = i

        if nlxline!=0 and nlyline!=0 and nlzline!=0 and npeline!=0 and npezline!=0 and ngtotline!=0:

            break

              

    nlx = int(re.search(r'\d+', nlxline).group())

    nly = int(re.search(r'\d+', nlyline).group())

    nlz = int(re.search(r'\d+', nlzline).group())

    npe = int(re.search(r'\d+', npeline).group())

    npez = int(re.search(r'\d+', npezline).group())

    ngtot = int(re.search(r'\d+', ngtotline).group())

    

    for j in lines:

        if j.find(' lx')!=-1:

            lxline = j

        if j.find(' ly')!=-1:

            lyline = j

        if j.find(' lz')!=-1:

            lzline = j

        if j.find(' rhoi ')!=-1:

            rhoiline = j

        if j.find('rhos ')!=-1:

            rhosline = j

        if j.find('de ')!=-1:

            deline = j

        if j.find('hyper_order')!=-1:

            hyper_orderline = j

        if j.find('hyper_order_g')!=-1:

            hyper_order_gline = j

        if j.find('hyper_morder')!=-1:

            hyper_morderline = j

        if lxline!=0 and lyline!=0 and lzline!=0 and rhoiline!=0 and rhosline!=0 and deline!=0 and hyper_orderline!=0 and hyper_order_gline!=0 and hyper_morderline!=0:

            break

    

    lx = float(re.search(r'\d+\.\d*', lxline).group())

    ly = float(re.search(r'\d+\.\d*', lyline).group())

    lz = float(re.search(r'\d+\.\d*', lzline).group())

    rhoi = float(re.search(r"\d+\.\d*", rhoiline).group())

    rhos = float(re.search(r"\d+\.\d*", rhosline).group())

    de = float(re.search(r"\d+\.\d*", deline).group()) # . \d+

    hyper_order = int(re.search(r'\d+', hyper_orderline).group())  

    hyper_order_g = int(re.search(r'\d+', hyper_order_gline).group())

    hyper_morder = int(re.search(r'\d+', hyper_morderline).group())

#    for k in lines:

#        if k.find('npe')!=-1:

#            npeline = k

#        if npeline!=0:

#            break

    return lx,ly,lz,nlx,nly,nlz,ngtot,npe,npez,rhoi,rhos,de,hyper_order,hyper_order_g,hyper_morder



def loading_field_data(filename):

    lx,ly,lz,nlx,nly,nlz,ngtot,npe,npez,rhoi,rhos,de = GetResolution(filename)

    filenm = filename

    filenmroot = filenm.split('_fields')[0]

    array_n = np.zeros((nlx,nly,nlz))

    array_apar = np.zeros((nlx,nly,nlz))

    points_per_proc = (nlx*nly*nlz)/(npe*npez)

    npp = npz = i = j = k = index = index_i = index_j = index_k = 0

    with open(filename,"r") as read_file:

        for line in read_file:

            array_apar[index_i,index_j,index_k]=line.split(None, 2)[0]

            array_n[index_i,index_j,index_k]=line.split(None, 2)[1]            

            index += 1 

            i = index%nlx

            k = (index//(nlx*nly/npe))%(nlz/npez)

            j = ((index)//(nlx))%(nly/npe)

            npz = index//(npe*points_per_proc)

            npp = (index-npe*npz*points_per_proc)//points_per_proc

            index_i = int(i)

            index_j = int(j+npp*nly/npe)

            index_k = int(k+npz*nlz/npez)

    return array_apar, array_n

        







#####################################################################################################

########## This is the segment loading gfield data#################################

        input_freq = 5

        for n in np.arange(0,len(timestamp),input_freq):

            filename = filestamp + '{:.3f}'.format(timestamp[n])+'.dat'

            gfilename = gfilestamp + '{:.3f}'.format(timestamp[n])+'.dat'

                     

            

            npp = npz = i = j = k = index = indexg = index_i = index_j = index_k = 0

            with open(gfilename,"r") as read_fileg:

                for count, line in enumerate(read_fileg, start=0):

                    moments_line = count % glines

                    if count % glines == 0 and count != 0:

                        indexg += 1 

                        i = indexg%nlx

                        k = (indexg//(nlx*nly/npe))%(nlz/npez)

                        j = ((indexg)//(nlx))%(nly/npe)

                        npz = indexg//(npe*points_per_proc)

                        npp = (indexg-npe*npz*points_per_proc)//points_per_proc

                        index_i = int(i)

                        index_j = int(j+npp*nly/npe)

                        index_k = int(k+npz*nlz/npez)

                    if moments_line != glines_1:

                        for w in range(3):

                            moments[int(moments_line*3+w+2),index_i,index_j,index_k] = line.split(None)[w]

                    else:

                        for e in range(g_num_ll):

                            moments[int(moments_line*3+e+2),index_i,index_j,index_k] = line.split(None)[e]

    

            npp = npz = i = j = k = index = indexg = index_i = index_j = index_k = 0            

    

            with open(filename,"r") as read_file:

                for line in read_file:

                    moments[0,index_i,index_j,index_k]=line.split(None, 1)[1] #density

                    moments[1,index_i,index_j,index_k]=line.split(None, 1)[0] #apar

                    index += 1 

                    i = index%nlx

                    k = (index//(nlx*nly/npe))%(nlz/npez)

                    j = ((index)//(nlx))%(nly/npe)

                    npz = index//(npe*points_per_proc)

                    npp = (index-npe*npz*points_per_proc)//points_per_proc

                    index_i = int(i)

                    index_j = int(j+npp*nly/npe)

                    index_k = int(k+npz*nlz/npez)        

    

            #computing the fourier transforms #SHIFTED (!) FFT

            for g in range(int(ngtot+1)):

                momentsk[g,:,:,:] =np.fft.fftshift( np.fft.fftn(moments[g,:,:,:])/(nlx*nly*nlz)) 

  ###################################################################################################################

  ###################################################################################################################              





####################################################################################################

###########################This part is calculating the dissipation in real space and velocity space#########

#####The "dissipation_coeffs: is loaded from the dataflie FILEROOT_hypercoeffs.dat########################## 



    kperpmax = int(np.sqrt((nlx/2)**2+(nly/2)**2))+1





    res2 = dissipation_coeffs[0]

    niu2 = dissipation_coeffs[1]

    nu_g = dissipation_coeffs[2]

    hyper_nuei = dissipation_coeffs[3]





    phik = np.zeros((nlx,nly,nlz),dtype=complex)



    for k in range(nlz):

        for j in range(nly):

            for i in range(nlx):

                kperp2 = (i-nlx/2)**2+(j-nly/2)**2

                phik[i,j,k] = rhoi**2/2*(Gamma0(kperp2*rhoi**2/2)-1)**(-1)*all_momentsk[0,i,j,k]



    #possible new version 

    hyper_viscosity = np.zeros((nlx,nly,nlz), dtype = complex)

    hyper_eta = np.zeros((nlx,nly,nlz), dtype = complex)

    hyper_collisions = np.zeros((nlx,nly,nlz),dtype = complex)



        

    for k in range(nlz):

        for j in range(nly):

            for i in range(nlx):

                kperp2 = (i-nlx/2)**2+(j-nly/2)**2

                hyper_viscosity[i,j,k] = 2.0*niu2*kperp2**hyper_order*(rhos**2*all_momentsk[0,i,j,k]-phik[i,j,k])#not absolute

                hyper_eta[i,j,k] = 2.0*res2*kperp2*kperp2**hyper_order*(all_momentsk[1,i,j,k]) #not absolute



    for g in range(2,Nmoments):          

         for k in range(nlz):

            for j in range(nly):

                for i in range(nlx):

                    kperp2 = (i-nlx/2)**2+(j-nly/2)**2

                    if g>=3:

                        hyper_collisions[i,j,k]  += 2*hyper_nuei*rhos**2*g**(2*hyper_morder)*(all_momentsk[g,i,j,k]) #not ABSOLUTE

                    

    hyper_collisions_r = np.abs(np.fft.ifftn(np.fft.ifftshift(hyper_collisions)))

    hyper_eta_r = np.abs(np.fft.ifftn(np.fft.ifftshift(hyper_eta)))

    hyper_viscosity_r = np.abs(np.fft.ifftn(np.fft.ifftshift(hyper_viscosity)))



