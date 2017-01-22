====
Glacier Tree Hash
====

Usage:
 ./treehash.py \'71.mp4
 Calculated: 0d4902d32750a09c7d7df5619d8685d0883f8ab2ae90cd47c01cbe394f75ab1e
 
 ./treehash.py -c 0d4902d32750a09c7d7df5619d8685d0883f8ab2ae90cd47c01cbe394f75ab1e \'71.mp4
 Checksums are equal!
 Calculated: 0d4902d32750a09c7d7df5619d8685d0883f8ab2ae90cd47c01cbe394f75ab1e
 
 ./treehash.py -j awscli-output.json \'71.mp4
 Checksums are equal!
 Calculated: 0d4902d32750a09c7d7df5619d8685d0883f8ab2ae90cd47c01cbe394f75ab1e
 

----
Performance
----

As a coincidence, it's about 4x faster than the java reference implementation
provided by Amazon
