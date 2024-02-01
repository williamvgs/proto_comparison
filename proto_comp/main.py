import sys
import argparse
import thruster_v15_pb2 
from google.protobuf import text_format
from google.protobuf import descriptor
from google.protobuf.descriptor_pool import Default

def get_descriptors(proto_module):
    descriptors = []

    for name, obj in vars(proto_module).items():
        if isinstance(obj, descriptor.Descriptor):
            descriptors.append(obj)

    return descriptors

def compare_descriptors(proto_descriptors, pb2_descriptors):
    return proto_descriptors == pb2_descriptors

def compare_proto_and_pb2(proto_file_path, pb2_module):
    # Load .proto file content
    with open(proto_file_path, 'r') as proto_file:
        proto_content = proto_file.read()

    # Parse .proto content into a message object
    proto_message = pb2_module.ThrusterParameters()
    text_format.Parse(proto_content, proto_message)

    # Create DescriptorPool directly
    pool = Default()
    pool.Add(proto_message)

    # Get descriptors from .proto and .pb2 file
    proto_descriptors = get_descriptors(pool.FindMessageTypeByName('ThrusterParameters'))
    pb2_descriptors = get_descriptors(pb2_module.ThrusterParameters.DESCRIPTOR)

    # Compare descriptors
    return compare_descriptors(proto_descriptors, pb2_descriptors)

if __name__ == "__main__":
    # Specify the path to your .proto file
    proto_file_path = 'old/proto_files/thruster_v15.proto'  
    
    # Compare .proto and .pb2 files
    match = compare_proto_and_pb2(proto_file_path, thruster_v15_pb2)

    if match:
        print("Descriptors match between .proto and .pb2 files.")
    else:
        print("Descriptors do not match.")
