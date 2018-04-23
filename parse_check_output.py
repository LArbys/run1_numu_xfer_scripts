import os,sys,subprocess


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

def makeup_partition_list( pathlist, outdir ):

    with open(pathlist, 'r') as f:
        
        for l in f:
            
            l = l.strip()
            fname = l.split('/')[-1]
            pnfsname = l.replace('/pnfs/', '/pnfs/fnal.gov/usr/')
            outname = outdir + '/' + fname

            if not os.path.exists(outname):
                print "File NOT already transferred: " + pnfsname
                cmd = "xrdcp xroot://fndca1.fnal.gov/%s %s"%(pnfsname,outname)
                print cmd
                x = os.popen(cmd)
                print x.readlines()

def check_partition_list( pathlist, outdir, resultfile, recopy=True ):
    """
    Compares server-side and local file checksums. Records results into resultfile
    Format of file
    filename RESULT SERVERSUM LOCALSUM

    RESULT codes:
    -2: Local file not found.
    -1: Difference found. Attempted transfer, still failed.
     0: Difference found. Did not attempt retransfer
     1: Good. checksums match
     2: Authentication error getting server checksum
    """

    result = open(resultfile,'w')
    with open(pathlist, 'r') as f:

        for l in f:

            l = l.strip()
            fname = l.split('/')[-1]
            pnfsname = l.replace('/pnfs', '/pnfs/fnal.gov/usr/')
            outname = outdir + '/' + fname

            if not os.path.exists(outname):
                print "File " + outname + " does not exist"
                print "Skipping check for this file ... please run makeup script"
                print >> result,os.path.basename(pnfsname),'\t',-2,'\t',"%08d"%(0),'\t',"%08d"%(0)
                continue

            source_cmd = "xrdfs xroot://fndca1.fnal.gov query checksum " + pnfsname
            #print source_cmd
            try:
                source_checksum = subprocess.check_output(source_cmd, shell=True).strip().split(' ')[-1]
                #print source_checksum
            except:
                print "Could not obtain checksum for file " + pnfsname
                print "Skipping check for this file..."
                print >> result,os.path.basename(pnfsname),'\t',2,'\t',"%08d"%(0),'\t',"%08d"%(0)
                continue

            local_cmd = "jacksum -a adler32 -E hex " + outname
            #print local_cmd
            local_checksum = subprocess.check_output(local_cmd, shell=True).strip().split()[0]
            #print local_checksum
                            

            if source_checksum != local_checksum:

                # Print out the file names
                print "File checksums NOT equal: "
                print "   Source: " + pnfsname
                print "   Local: " + outname


                if recopy:
                    # Remove the local file
                    rm_cmd = "rm " + outname
                    print rm_cmnd
                    subprocess.call(rm_cmd, shell=True)
                
                # Try to re-copy
                    cmd = "xrdcp xroot://fndca1.fnal.gov/%s %s"%(pnfsname,outname)
                    print cmd
                    x = subprocess.check_output(cmd, shell=True)
                    print x

                # Print result
                    local_checksum = subprocess.check_output(local_cmd, shell=True).strip().split()[0]
                    print local_checksum
                    if source_checksum == local_checksum:
                        print "File checksums reconciled for " + fname
                        print >> result,os.path.basename(pnfsname),'\t',1,'\t',source_checksum,'\t',local_checksum
                    else:
                        print "File checksnums NOT reconciled for " + fname
                        print >> result,os.path.basename(pnfsname),'\t',-1,'\t',source_checksum,'\t',local_checksum
                else:
                    print "in debug mode only (recopy=False)."
                    print >> result,os.path.basename(pnfsname),'\t',0,'\t',source_checksum,'\t',local_checksum
            else:
                print >> result,os.path.basename(pnfsname),'\t',1,'\t',source_checksum,'\t',local_checksum
                
    result.close()
    return None

if __name__=="__main__":

    # for larcv
    pathlist_stem = "pathlists/pathlist_tmw_prod_larcv_optfilter_bnb_v11_mcc8_p%02d.txt"

    # for larlite opreco
    #pathlist_stem = "pathlists/larlite_opreco/pathlist_tmw_prod_larlite_optfilter_opreco_bnb_v11_mcc8_p%02d"

    # for larlite reco2d
    #pathlist_stem = "pathlists/larlite_reco2d/pathlist_tmw_prod_larlite_optfilter_reco2d_bnb_v11_mcc8_p%02d"

    for p in range(0,20):
        outdir = "/cluster/kappa/90-days-archive/wongjiradlab/wselig01/larcv/p%02d"%(p)
        resultfile = "larcv_checksum_results_p%02d.txt"%(p)
        #outdir = "/cluster/kappa/90-days-archive/wongjiradlab/wselig01/larlite_opreco/p%02d"%(p)
        #outdir = "/cluster/kappa/90-days-archive/wongjiradlab/wselig01/larlite_reco2d/p%02d"%(p)
        
        results = [0, 0, 0, 0, 0]

        with open(resultfile, 'r') as f:
            for l in f:
                result_code = int(l.strip().split()[1])
                results[result_code + 2] += 1

        print "Results for " + str(p) + ":"
        for i in range(len(results)):
            if i != 3 and results[i] != 0:
                print "    files with exit code " + str(i-2) + ": " + str(results[i])
