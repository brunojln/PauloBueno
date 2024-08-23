from dataclasses import dataclass
import org.jblas.DoubleMatrix

@dataclass
class DataObject:
    h_path: str
    g: DoubleMatrix
    selected_algorithm: str
    selected_model_flag: int
    client_id: str
    signal_path: str

    @property
    def text(self):
        return f"\nAlgorithm: {self.selected_algorithm}\nH: {self.h_path}\ng: {self.signal_path}\nClientId: {self.client_id}\n"