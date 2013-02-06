from abc import ABCMeta, abstractmethod
from ungridded_data import UngriddedData
import sys

class AProduct(object):
    """
        Abstract class for the various possible data products. This just defines the interface which
         the subclasses must implement.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_ungridded_data(self, filenames, variable):
        """
        Create a an ungridded data object for a given variable from many files

        @param filenames:    List of filenames of files to read
        @param usr_variable:    Variable to read from the files
        @return: An UngriddedData object for the specified variable

        @raise FileIOError: Unable to read a file
        @raise InvalidVariableError: Variable not present in file
        """
        pass

class Cloudsat_2B_CWC_RVOD(AProduct):

    def create_ungridded_data(self, filenames, usr_variable):
        from read_ungridded import read_hdf4
        import utils
        import hdf_vd as hdf_vd
        import hdf_sd as hdf_sd

        if not isinstance(filenames,list): filenames = [ filenames ]

        variables = [ usr_variable, 'Latitude','Longitude','TAI_start','Profile_time','Height']

        all_sdata = {}
        all_vdata = {}
        for filename in filenames:
            sdata, vdata = read_hdf4(filename,variables)
            for varname in sdata.keys():
                utils.add_element_to_list_in_dict(all_sdata,varname,sdata[varname])
            for varname in vdata.keys():
                utils.add_element_to_list_in_dict(all_vdata,varname,vdata[varname])

        lat = utils.concatenate(all_vdata['Latitude'],hdf_vd.get_data)
        lon = utils.concatenate(all_vdata['Longitude'],hdf_vd.get_data)
        alt = utils.concatenate(all_sdata['Height'],hdf_sd.get_data)

        time = utils.concatenate(all_vdata['Profile_time'],hdf_vd.get_data) + utils.concatenate(all_vdata['TAI_start'],hdf_vd.get_data)

        all_vdata.pop('Latitude')
        all_vdata.pop('Longitude')
        all_sdata.pop('Height')
        all_vdata.pop('TAI_start')
        all_vdata.pop('Profile_time')

        if usr_variable in all_sdata.keys():
            return UngriddedData(all_sdata[usr_variable],lat,lon,alt,time,'HDF_SD')
        elif usr_variable in all_vdata.keys():
            return UngriddedData(all_vdata[usr_variable],lat,lon,alt,time,'HDF_VD')



def get_data(product, filenames, variable):
    """
        Top level routine for calling the correct product's create_ungridded_data routine.

    @param product: The product to read data from - this should be a string which matches the name of one of the subclasses of AProduct
    @param filenames: A list of filenames to read data from
    @param variable: The variable to create the UngriddedData object from
    @return: An Ungridded data variable
    """
    product_cls = None
    for cls in AProduct.__subclasses__():
        if product == cls.__name__:
            product_cls = cls
    if product_cls is None:
        raise(NotImplementedError)
    else:
        data = product_cls().create_ungridded_data(filenames, variable)
    return data