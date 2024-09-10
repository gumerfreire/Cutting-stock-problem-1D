import pandas as pd

class csp_1D:
    '''
    CUTTING STOCK PROBLEM
    2024. Gumer Freire
    gumerfreire@gmail.com

    Class for implementing solutions of the 1D optimization cutting stock problem.
    Different algorithms may be implemented in this class.
    '''

    def __init__(self, raw_length, piece_lengths=[], demand=[]):
        '''
        Inicializa el objeto 1D_Optimizer. Debe proporcionarse al menos la longitud de material en bruto.
        Los argumentos de longitudes y número de piezas de corte son opcionales, ya que se pueden incorporar
        los datos a través de una función específica para importar a partir de archivos.

        Input:
        raw_length: longitud de las barras de material en bruto
        piece_lengths: Lista de longitudes de corte de piezas
        demand: Lista de cantidades de piezas de cada longitud de corte
        '''

        #Initialize variables
        self.raw_length = raw_length
        self.piece_lengths = piece_lengths
        self.demand = demand
    
    def import_csv(self, filename, columnName_lengths='Length', columnName_demand='Quantity'):
        '''
        Imports data from a CSV file using a pandas dataframe

        Input:
        filename: Name of CSV file to import
        columnName_lengths: Name of the column in the CSV containing the lengths to cut
        columnName_demand: Name of the column in the CSV containing the number of units to cut of each length
        '''
        dataframe = pd.read_csv(filename)

        self.piece_lengths = dataframe[columnName_lengths].tolist()
        self.demand = dataframe[columnName_demand].tolist()

    def solve(self):

        #Preprocessing of data
        #Check if empty data and assign default demand in case of not having demand data.
        if len(self.piece_lengths) == 0:
            raise ValueError('The list of pieces to cut is empty. Please import some data')
        elif len(self.piece_lengths) > 0 and len(self.demand) == 0:
            print('Demand list empty. A default demand of 1 to each cut length is assigned')
            self.demand = [1] * len(self.piece_lengths)
        #Check if the list of lengths and demands have the same len.
        if len(self.piece_lengths) != len(self.demand):
            raise ValueError('The list of lengths and the list of demands must have the same number of values')

        #Solve using greedy algorithm
        # (more algorithms could be implemented for different solving procedures)    
        configurations, stock_used, waste = self.CSP_greedy()
        use_percentage = round(((stock_used * self.raw_length)-sum(waste)) / (stock_used * self.raw_length) * 100,1)
        
        #Print the results
        print("Cortes por pieza:")
        for i, config in enumerate(configurations):
            print(f"Pieza {i + 1}: {config} (Desperdicio: {waste[i]})")
        
        print(f"\nLongitud de piezas en bruto: {self.raw_length}")
        print(f"Piezas totales utilizadas: {stock_used}")
        print(f"Desperdicio total: {sum(waste)}")
        print(f"Aprovechamiento del material: {use_percentage} %")

    #Algorithms for solving the CSP problem. More than one algorithm may be implemented for different approaches.
    def CSP_greedy(self):
        """
        Function to solve the cutting stock problem using a greedy aalgorithm.
        
        Input:
        raw_length: Length of the raw material (1D)
        piece_lengths: List of lengths for the pieces you need
        demand: List of how many pieces of each length are needed

        Returns:
        cutting_configurations: List of cut lengths for each raw piece
        used_stock: Total nomber of raw pieces used
        waste_per_stock: Length of waste for each piece
        """
        
        # Create a list of pieces required by length
        pieces_required = []
        for length, count in zip(self.piece_lengths, self.demand):
            pieces_required.extend([length] * count)
        
        # Sort pieces in descending order (greedy choice: largest pieces first)
        pieces_required.sort(reverse=True)
        
        # Initialize result variables
        used_stock = 0
        waste_per_stock = []
        
        # Store stock cutting configurations
        cutting_configurations = []
        
        while pieces_required:
            used_stock += 1
            remaining_length = self.raw_length
            current_cutting = []
            
            for piece in pieces_required[:]:
                if piece <= remaining_length:
                    # Cut the piece from the raw material
                    remaining_length -= piece
                    current_cutting.append(piece)
                    pieces_required.remove(piece)
            
            cutting_configurations.append(current_cutting)
            waste_per_stock.append(remaining_length)
        
        return cutting_configurations, used_stock, waste_per_stock


#EJECUCION
#opt = csp_1D(6000,[2800,1050,3250,700,1050,3140,3580,2200,3073,1050,3130,3640,2450,2825,3225],[1,1,1,1,1,1,2,2,1,1,1,1,2,2,2])
#opt.solve()

opt = csp_1D(6000)
opt.import_csv('datasample.csv','Longitud','Unidades')
opt.solve()