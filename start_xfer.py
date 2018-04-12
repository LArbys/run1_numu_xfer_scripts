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
        if os.path.exists(outname):
            print "Already transferred"
            continue
        cmd = "xrdcp xroot://fndca1.fnal.gov/%s %s"%(pnfsname,outname)
        print cmd
        x = os.popen(cmd)
        print x.readlines()


if __name__=="__main__":

    # for larcv (restarted at 16,x,x)
    #pathlist_stem = "pathlists/pathlist_tmw_prod_larcv_optfilter_bnb_v11_mcc8_p%02d.txt"

    # for larlite opreco
    pathlist_stem = "pathlists/larlite_opreco/pathlist_tmw_prod_larlite_optfilter_opreco_bnb_v11_mcc8_p%02d"

    # for larlite reco2d
    #pathlist_stem = "pathlists/larlite_reco2d/pathlist_tmw_prod_larlite_optfilter_reco2d_bnb_v11_mcc8_p%02d"

    for p in range(0,20):
        #outdir = "/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/run1_numu/output/larcv/p%02d"%(p)
        #outdir = "/cluster/kappa/90-days-archive/wongjiradlab/wselig01/larcv/p%02d"%(p)
        outdir = "/cluster/kappa/90-days-archive/wongjiradlab/wselig01/larlite_opreco/p%02d"%(p)
        transfer_partition_list( pathlist_stem%(p), outdir )
        
