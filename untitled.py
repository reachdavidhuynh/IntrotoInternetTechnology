
    # send the size of the file as a 4 byte integer
    # to the server, so it knows how much to read
    FRAGMENTSIZE = 8192
    longPacker = struct.Struct("!L")
    fileLenPacked = longPacker.pack(filesize);
    s.send(fileLenPacked)

    # use the MD5 hash algorithm to validate all the data is correct
    mdhash = md5.new()

    # loop for the size of the file, sending the fragments
    bytes_to_send = filesize

    start_stamp = time.clock()
    while (bytes_to_send > 0):
        fragment = fd.read(FRAGMENTSIZE)
        mdhash.update(fragment)
        totalsent = 0
        # make sure we sent the whole fragment
        while (totalsent < len(fragment)):
            sent = s.send(fragment[totalsent:])
            if (sent == 0):
                raise RuntimeError("socket broken")
            totalsent = totalsent + sent
        bytes_to_send = bytes_to_send - len(fragment)

    end_stamp = time.clock()
    lapsed_seconds = end_stamp - start_stamp
    # this part send the lenght of the digest, then the
    # digest. It will be check on the server
'''
    digest = mdhash.digest()
    # send the length of the digest
    long = len(digest)
    digestLenPacked = longPacker.pack(long)
    sent = s.send(digestLenPacked)
    if (sent != 4):
        raise RuntimeError("socket broken")

    # send the digest
    sent = s.send(digest)
    if (sent != len(digest)):
        raise RuntimeError("socket broken")

    if (lapsed_seconds > 0.0):
        print ("client1: sent %d bytes in %0.6f seconds, %0.6f MB/s " % (filesize, lapsed_seconds, (filesize/lapsed_seconds)/(1024*1024)))
    else:
        print ("client1: sent %d bytes in %d seconds, inf MB/s " % (filesize, lapsed_seconds))

    fd.close()
    s.close()
# this gives a main function in Python
if __name__ == "__main__":
    main()

