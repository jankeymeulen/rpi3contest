#!/usr/bin/env python
import datetime
import sys
from gcloud import datastore

# create datastore client
client = datastore.Client("cafefritkotqueue")

# put it in the cloud
key = client.key("QueueLength")
entry = datastore.Entity(key)
entry.update({
	"Timestamp": datetime.datetime.utcnow(),
	"Length": int(sys.argv[1])
})
client.put(entry)
