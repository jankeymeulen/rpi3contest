package contest

import (
        "net/http"
        "time"
        "appengine"
        "appengine/datastore"
	"encoding/json"
)

type QueueLength struct {
   Length      int
   Timestamp   time.Time
}

func init() {
    http.HandleFunc("/", handler)
}

func handler(w http.ResponseWriter, r *http.Request) {

        c := appengine.NewContext(r)

        q := datastore.NewQuery("QueueLength").Order("-Timestamp").Limit(360)
        queuelengths := make([]QueueLength, 0, 360)
        if _, err := q.GetAll(c, &queuelengths); err != nil {
                http.Error(w, err.Error(), http.StatusInternalServerError)
                return
        }
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(queuelengths)
}
