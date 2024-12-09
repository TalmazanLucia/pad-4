import cls from './Clothes.module.scss';
import {useEffect, useState} from "react";

const Clothes = ({selectedCategory}) => {
    const [data, setData] = useState([]);

    const getData = async () => {
        const response = await fetch(selectedCategory
            ? `http://138.68.76.97/api/clothes?category_id=${selectedCategory}`
            : `http://138.68.76.97/api/clothes`
        );
        const json = await response.json();

        setData(json ? json : [])
    }

    useEffect(() => {
        getData();
    }, [selectedCategory]);

    return (
        <div>
            <div className={cls.clothesWrapper}>
                {data.map((cloth, index) => (
                    <div key={index} className={cls.clothWrapper}>
                        <p className={cls.clothName}>{cloth.name}({cloth.color})</p>
                        <p><i>{cloth.description}</i></p>
                        <p>{cloth.size} - {cloth.material}</p>
                        <div className={cls.dataRow}>
                            <p>{cloth.rating}</p>
                            <p>{cloth.price}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Clothes;