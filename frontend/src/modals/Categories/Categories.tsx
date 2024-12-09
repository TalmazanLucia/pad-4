import {useEffect, useState} from "react";
import cls from './Categories.module.scss';

const Categories = ({handleSelect}) => {
    const [data, setData] = useState([]);

    const getData = async () => {
        const response = await fetch('http://138.68.76.97/api/categories');
        const json = await response.json();

        setData(json)

    }

    useEffect(() => {
        getData();
    }, []);

    return (
        <div className={cls.categoriesWrapper}>
            {data.map((category, index) => (
                <div key={index} className={cls.category} onClick={() => handleSelect(category.id)}>{category.name}</div>
            ))}
        </div>
    );
};

export default Categories;