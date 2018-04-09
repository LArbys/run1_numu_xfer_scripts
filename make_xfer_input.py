import os,sys


def transfer_partition_list( pathlist, outdir ):

    os.system("mkdir -p %s"%(outdir))

    f = open(pathlist,'r')
    lines = f.readlines()
    f.close()

    print "Number of events in list: " ,len(lines)

    for l in lines:
        l = l.strip()
        pieces = l.split("/")
        pnfsname = l.strip().replace("/pnfs/","/pnfs/fnal.gov/usr/").strip()
        outname = outdir + "/" + pieces[-1]
        cmd = "xrdcp xroot://fndca1.fnal.gov/%s %s"%(pnfsname,outname)
        print cmd
        #x = os.popen(cmd)
        #print x.readlines()


if __name__=="__main__":

    outdir = "/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/run1_numu/output/larcv/p00"
    transfer_partition_list( "pathlists/pathlist_tmw_prod_larcv_optfilter_bnb_v11_mcc8_p00.txt", outdir )

