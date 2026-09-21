import re
import gzip
import csv
from Bio.Seq import Seq
from Bio import SeqIO

log_lines = [
    "2024-01-15 10:02:11 INFO Server started on port 8080",
    "2024-01-15 10:03:47 ERROR Failed to connect to database",
    "2024-01-16 08:15:00 WARNING Disk usage at 85%",
    "2024-01-16 14:22:39 ERROR Timeout while fetching https://example.com/api",
    "2024-01-17 09:00:05 INFO User admin logged in from 192.168.1.10",
    "2024-01-17 11:41:18 DEBUG Cache cleared successfully",
    "2024-01-18 03:12:56 ERROR Connection refused from 192.168.1.55",
    "2024-01-18 23:59:02 INFO Backup completed in 42s",
]
logs1 =[]
logs2 =[]
logs3 =[]
logs4 =[]
logs5 =[]
logs6 =[]
for line in log_lines:
    if re.match(r"2024-01-16", line) != None:
        logs1.append(line)
    if re.search(r"ERROR|WARNING",line) != None:
        logs2.append(line)
    if re.search(r"(\d{1,3}\.){3}\d{1,3}",line) != None:
        logs3.append(line)
    if re.search(r"\d+s$",line) != None:
        logs4.append(line)
    if re.search(r".*http://|https://.*",line) != None:
        logs5.append(line)
    if re.fullmatch(r"^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\s.+",line) != None:
        #print("good")
        logs6.append(line)
    #else:
        #print("bad")
#print(logs6)
def reverse_complement(seq_obj):
    seq_obj = Seq(seq_obj)
    rev_comp = str(seq_obj.reverse_complement())
    print("rev:comp")
    return rev_comp

class SequencingRead:
    def __init__(self,read_id,sequence):
        self.read_id = read_id
        self.sequence = sequence
    def matches_mid_pair(self, forward_mid, reverse_mid):
        if re.match(f"^{forward_mid}.+{reverse_mid}$",self.sequence) != None :
            return True
        else:
            return False
    def trim_mid_pair(self, forward_mid, reverse_mid):
        if self.matches_mid_pair(forward_mid,reverse_mid) == True :
            return (self.sequence[len(forward_mid):-len(reverse_mid)])
        else:return(print("what"))

    def describe(self):
        print(f"Seauencing read {self.read_id} ({len(self.sequence)} bp)")

class SequencingRead:
    def __init__(self,record_id,record):
        self.record_id=record_id
        self.record = record


class Demultiplexer:
    assigned = {}
    unassigned = []
    def __init__(self, fasta_path, mid_table_path,assigned,unassigned):
        self.reads= self.parse_fasta(fasta_path)
        self.mid_list = self.parse_mid_table(mid_table_path)
        self.assigned=assigned
        self.unassigned=unassigned

    def parse_fasta(self,fasta_path):
        # Open gzip file in text mode for SeqIO
        reads=[]
        with gzip.open(fasta_path, "rt") as handle:
            for record in SeqIO.parse(handle, "fasta"):
                reads.append(SequencingRead(record.id,str(record.seq)))
    def parse_mid_table(self,mid_table_path):
        tuples_list=[]
        with open(mid_table_path, newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle, delimiter=";")
            required_fields = {"SampleID", "FBarcodeSequence", "RBarcodeSequence", "Description"}

            # Validate header
            if not required_fields.issubset(reader.fieldnames or []):
                raise ValueError(f"CSV is missing required columns: {required_fields - set(reader.fieldnames or [])}")

            for row in reader:
                sample_id = row["SampleID"].strip()
                f_barcode = row["FBarcodeSequence"].strip()
                r_barcode = row["RBarcodeSequence"].strip()
                description = row["Description"].strip()

                label = f"{sample_id}_{description}"
                tuples_list.append((label, f_barcode, r_barcode))
        return tuples_list

    def assign_reads(self):
        for read in self.reads:
            for mid in self.mid_list:
                forward_mid = mid[1]
                reverse_mid = mid[2]
                if re.match(f"^{forward_mid}.+{reverse_complement(reverse_mid)}$",self.sequence) != None :

                elif re.match(f"^{reverse_mid}.+{reverse_complement(forward_mid)}$",self.sequence) != None :

                else:
                    return None







